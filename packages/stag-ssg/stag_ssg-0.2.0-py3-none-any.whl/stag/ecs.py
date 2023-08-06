from __future__ import annotations

import os
from collections import UserDict, defaultdict
from datetime import date as _date_t
from datetime import datetime as _datetime_t
from urllib.parse import urlparse, urljoin
from functools import cache

from typing import Union as _Union
from typing import Optional as _Optional
from typing import Any as _Any
from collections.abc import Mapping as _Mapping

import attr
from dateutil.parser import parse as _parse_dt

from stag.signals import signal, signals


# sentinel used for parameters for which None is a valid value
_ANY = "_ANY"


def _urlize(url):
    url = url.strip("/")
    return f"/{url}"


def _absurl(base, path):
    return urljoin(base, path)


@attr.s(auto_attribs=True, frozen=True)
class Path:
    path: str
    root_dir: str

    @property
    def relpath(self):
        return self.path[len(self.root_dir) :].strip("/")

    @property
    def ext(self):
        return os.path.splitext(self.path)[1][len(os.extsep) :]

    @property
    def filebase(self):
        return os.path.splitext(self.basename)[0]

    @property
    def basename(self):
        return os.path.basename(self.path)

    @property
    def reldirname(self):
        return os.path.dirname(self.relpath)


@attr.s(auto_attribs=True)
class Content:
    type: str
    content: _Any = attr.ib(None, repr=False)


class Metadata(UserDict):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._normalize_data()

    def _normalize_data(self):
        title = self.data.get("title", "")
        date = self.data.get("date")
        if date:
            if isinstance(date, (int, str, float)):
                self.data["date"] = _parse_dt(date)
            elif type(date) == _date_t:
                self.data["date"] = _datetime_t.fromordinal(date.toordinal())
            self.data["timestamp"] = self.data["date"].timestamp()

        self.__dict__.update(self.data)


@attr.s(auto_attribs=True)
class Taxonomy:
    name: str
    singular: str
    plural: str
    terms: _List[Page] = attr.ib(factory=list, repr=False)


@attr.s(auto_attribs=True)
class Term:
    name: str
    pages: _List[Page] = attr.ib(factory=list)


class _Notified:
    """Descriptor of fields which should automatically notify some of their
    changes."""

    def __init__(self, name):
        self.name = name
        self.real = "_" + name

    def __get__(self, obj, objtype):
        return getattr(obj, self.real)

    def __set__(self, obj, val):
        curr = getattr(obj, self.real)
        setattr(obj, self.real, val)

        # emit signals
        if val is None and curr is not None:
            signame = f"{self.name}_removed"
            getattr(obj, signame).emit(obj, curr)
        elif val != curr:
            signame = f"{self.name}_created"
            getattr(obj, signame).emit(obj, val)


def component(type_, **kw):
    kw.setdefault("metadata", {})["component"] = True
    kw.setdefault("repr", False)
    return attr.ib(None, **kw)


def component_descriptors(cls):
    for a in cls.__attrs_attrs__:
        if a.metadata and a.metadata.get("component"):
            dname = a.name.lstrip("_")
            setattr(cls, dname, _Notified(dname))

    return cls


@component_descriptors
@attr.s(auto_attribs=True, cmp=False, hash=False)
class Page:
    _url: str = attr.ib(converter=urlparse)

    _metadata: _Optional[Metadata] = component(Metadata)
    _source: _Optional[Path] = component(Path)
    _input: _Optional[Content] = component(Content)
    _output: _Optional[Content] = component(Content)
    _taxonomy: _Optional[Taxonomy] = component(Taxonomy)
    _term: _Optional[Term] = component(Term)

    def __attrs_post_init__(self):
        for a in self.__attrs_attrs__:
            dname = a.name.lstrip("_")
            if a.metadata and a.metadata.get("component"):
                crsig = f"{dname}_created"
                setattr(self, crsig, signal(crsig))
                rmsig = f"{dname}_removed"
                setattr(self, rmsig, signal(rmsig))

    @property
    @cache
    def url(self):
        return self._url.geturl()

    @property
    @cache
    def relurl(self):
        return self._url.path

    @property
    def md(self):
        return self._metadata

    def __hash__(self):
        return hash(self._url)

    def __eq__(self, other):
        return self._url == other._url

    def __lt__(self, other):
        return self._url < other._url


@attr.s(auto_attribs=True)
class Site:
    config: dict = attr.ib(repr=False)
    _pages: _Mapping[str, Page] = attr.ib(factory=dict, repr=False)
    taxonomies: _Optional[list[Taxonomy]] = attr.ib(None, repr=False)

    # signals
    page_added: signal = attr.ib(
        factory=lambda: signal("page_added"), repr=False, init=False
    )

    @property
    def pages(self):
        return list(self._pages.values())

    @property
    def ordinary_pages(self):
        for page in self._pages.values():
            if page.source and page.input and page.output and page.metadata:
                yield page

    def subpages_of(self, val, recursive=False):
        def _cmp(pardir, exp):
            return pardir == exp

        def _cmp_r(pardir, exp):
            cp = os.path.commonpath([pardir, exp])
            return cp == exp

        cmp_fn = _cmp_r if recursive else _cmp

        base = _urlize(val)
        for page in self.ordinary_pages:
            pardir = os.path.dirname(page.relurl)
            if cmp_fn(pardir, base):
                yield page

    def make_page(self, path, **kw):
        path = _urlize(path)
        if path in self._pages:
            raise ValueError(f"URL {path} already exists")

        url = _absurl(self.config.url, path)
        page = Page(url, **kw)
        self._pages[path] = page
        self.page_added.emit(page)
        return page

    def get_or_make_page(self, path, **kw):
        path = _urlize(path)
        if path in self._pages:
            return self._pages[path]

        url = _absurl(self.config.url, path)
        page = Page(url, **kw)
        self._pages[path] = page
        self.page_added.emit(page)
        return page

    def filter_pages(self, ptype=_ANY):
        for page in self.pages:
            if page.metadata is not None and ptype is _ANY:
                yield page
            elif page.metadata is not None and page.metadata.get("type", _ANY) == ptype:
                yield page

    def find(self, path):
        return self._pages.get(_urlize(path))
