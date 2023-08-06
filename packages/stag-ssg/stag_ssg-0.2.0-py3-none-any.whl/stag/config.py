import os
import copy
from functools import cache

from typing import Optional, Any

import attr
import tomli

from stag.utils import attr_access


class ConfigError(Exception):
    pass


@attr.s(auto_attribs=True)
class TemplateTable:
    name: str = os.path.join("themes", "default")
    templates: dict = attr.ib(factory=dict, converter=attr_access)

    def __attrs_post_init__(self):
        self.templates.setdefault("page", "page")
        self.templates.setdefault("list", "list")
        self.templates.setdefault("taxonomy", "taxonomy")


@attr.s(auto_attribs=True)
class TaxonomyTable:
    key: str
    singular: Optional[str] = None
    plural: Optional[str] = None

    def __attrs_post_init__(self):
        if self.singular is None:
            self.singular = self.key
        if self.plural is None:
            self.plural = self.key


def init_table(cls):
    def _init(val):
        if isinstance(val, dict):
            return cls(**val)
        if isinstance(val, (tuple, list)):
            return type(val)(cls(**elem) for elem in val)
        if isinstance(val, cls):
            return val
        return cls(val)

    return _init


@attr.s(auto_attribs=True)
class Config:
    title: str = "MySite"
    url: str = "https://example.com"
    language: str = "en"
    timezone: str = "+0000"
    pluginspath: str = "plugins"
    content: str = "content"
    output: str = "_output"
    taxonomies: list[TaxonomyTable] = attr.ib(
        factory=list, converter=init_table(TaxonomyTable)
    )
    template: TemplateTable = attr.ib(
        factory=TemplateTable, converter=init_table(TemplateTable)
    )
    user: Any = attr.ib(factory=dict, converter=attr_access)
    plugins: Any = attr.ib(factory=dict, converter=attr_access)

    def get(self, name, default=None):
        return getattr(self, name, default)

    def update_plugin_table(self, name, table):
        if name in self.plugins:
            vals = self.plugins[name]
            if hasattr(table, "__attrs_attrs__"):
                try:
                    self.plugins[name] = attr.evolve(table, **vals)
                except TypeError as e:
                    raise ConfigError(
                        f"Configuration error in plugins.{name} table: {e}"
                    )
            else:
                newtable = copy.deepcopy(table)
                newtable.__dict__.update(vals)
                self.plugins[name] = newtable
        else:
            self.plugins[name] = table


@cache
def read_config(path):
    try:
        with open(path) as f:
            config_dct = tomli.loads(f.read())
    except FileNotFoundError:
        config_dct = {}

    return Config(**config_dct)
