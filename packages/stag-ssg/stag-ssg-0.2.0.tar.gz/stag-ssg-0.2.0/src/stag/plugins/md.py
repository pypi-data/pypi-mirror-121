import os
import itertools

from typing import List

import attr
import tomli
import markdown

from stag.ecs import Page, Content, Metadata
from stag.signals import signals, condition
from stag.reading import readers
from stag.plugins._helpers import read_file


def is_md(page):
    return page.source and page.source.ext == "md"


def is_opened_md(page):
    return page.input and page.input.type == "md"


@attr.s(auto_attribs=True)
class MarkdownConfig:
    extensions: List[str] = attr.Factory(lambda: ["footnotes", "fenced_code", "smarty"])


def deduce_url(path):
    if path.filebase == "index":
        return path.reldirname
    return os.path.join(path.reldirname, path.filebase)


def read(page):
    if not is_md(page):
        return

    metadata, content, _ = read_file(page.source.path)
    page.metadata = Metadata(metadata)
    page.input = Content("md", content)


def generate(site):
    myconfig = site.config.plugins.markdown
    conv = markdown.Markdown(extensions=myconfig.extensions)

    for page in site.pages:
        if not is_opened_md(page):
            continue

        assert "title" in page.metadata, f"No title in {page.source.relpath}"
        html = conv.reset().convert(page.input.content)
        page.output = Content("html", html)


def register_plugin():
    signals.site_init.connect(
        lambda s: s.config.update_plugin_table("markdown", MarkdownConfig()), weak=False
    )
    signals.readers_init.connect(
        (lambda site: site.page_added.connect(read)), weak=False
    )
    signals.processors_init.connect(generate)
    readers.register_reader(deduce_url, lambda p: p.ext == "md")
