import os
from datetime import datetime

import tomli

from stag.signals import signals, condition
from stag.reading import readers
from stag.ecs import Page, Content, Metadata
from stag.plugins._helpers import read_file


def is_xml(page):
    return page.source and page.source.ext == "xml"


def read(page):
    if not is_xml(page):
        return

    md, cn, _ = read_file(page.source.path)
    md.setdefault("title", page.source.filebase.capitalize())
    md.setdefault("type", page.source.filebase)
    md.setdefault("date", datetime.now())
    page.metadata = Metadata(md)
    page.input = Content("xml", cn)
    page.output = Content("xml", cn)


def register_plugin():
    signals.readers_init.connect(
        (lambda site: site.page_added.connect(read)), weak=False
    )
