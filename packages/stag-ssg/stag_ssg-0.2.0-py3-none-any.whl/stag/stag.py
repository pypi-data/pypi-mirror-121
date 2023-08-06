import os
import sys
import argparse
import shutil
import logging
import pkgutil
from copy import deepcopy

from stag.config import read_config
from stag.ecs import Site, Path, Page
from stag.utils import chdir
from stag.signals import signals
from stag.reading import readers
from stag.writing import render
from stag._version import version

log = logging.getLogger(__name__)


def load_plugins(paths):
    for finder, name, ispkg in pkgutil.iter_modules(paths):
        if name.startswith("_"):
            continue

        found = finder.find_module(name)
        if found:
            mod = found.load_module()
            try:
                mod.register_plugin()
            except AttributeError as e:
                log.error(f"{e} - plugin will be disabled")


def build(args):
    config = read_config(args.config)
    override_config_with_commandline_args(config, args)

    log.info(f"Building site to {config.output}")

    shutil.rmtree(config.output, ignore_errors=True)
    os.makedirs(config.output)

    builtin = os.path.join(os.path.dirname(__file__), "plugins")
    load_plugins([builtin, config.pluginspath])
    signals.plugins_loaded.emit()

    site = Site(config=config)
    signals.site_init.emit(site)

    roots = [
        config.content,
        os.path.join(config.template.name, "static"),
        "static",
    ]

    signals.readers_init.emit(site)

    for root in roots:
        gather_files(root, site)

    signals.readers_finished.emit(site)

    signals.processors_init.emit(site)
    signals.processors_finished.emit(site)

    signals.rendering_init.emit(site)
    render(site)
    signals.rendering_finished.emit(site)

    signals.site_finished.emit(site)


def serve(args):
    from http.server import HTTPServer, SimpleHTTPRequestHandler

    config = read_config(args.config)
    override_config_with_commandline_args(config, args)

    build(args)
    with chdir(config.output):
        log.info(f"Running simple HTTP server on http://localhost:{args.port}.")
        server_address = ("", args.port)
        httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
        httpd.serve_forever()


def deduce_url(path):
    if path.filebase == "index":
        return path.reldirname
    else:
        slug, _ = os.path.splitext(path.basename)
        return os.path.join(path.reldirname, pat.filebase)


def gather_files(srcdir, site):
    for curdir, _, files in os.walk(srcdir):
        for f in files:
            path = Path(os.path.join(curdir, f), srcdir)
            relurl = readers.get_path(path)
            site.make_page(relurl, source=path)


def override_config_with_commandline_args(config, args):
    for name, val in args.__dict__.items():
        if val is not None and hasattr(config, name):
            setattr(config, name, args.__dict__[name])


def prepare_args(argv):
    parser = argparse.ArgumentParser(description="Simply Stupid Static Site Generator")
    parser.set_defaults(verbosity=logging.INFO)

    parser.add_argument(
        "-c",
        "--config",
        nargs="?",
        default="config.toml",
        help="path to stag's configuration file",
    )

    parser.add_argument(
        "-D",
        "--debug",
        action="store_const",
        const=logging.DEBUG,
        dest="verbosity",
        help="show debug messages",
    )

    parser.add_argument("--version", action="version", version=f"%(prog)s {version}")

    sp = parser.add_subparsers(required=True, dest="subcommands")

    sp_build = sp.add_parser("build")
    sp_build.add_argument("-o", "--output", help="output directory")
    sp_build.set_defaults(func=build)

    sp_serve = sp.add_parser("serve")
    sp_serve.add_argument("-o", "--output", help="output directory")
    sp_serve.add_argument("-p", "--port", type=int, default="8000", help="HTTP port")
    sp_serve.set_defaults(func=serve)

    return parser.parse_args(argv)


def main_(argv):
    args = prepare_args(argv)
    logging.basicConfig(format="%(message)s", level=args.verbosity)

    try:
        return args.func(args)
    except Exception as e:
        log.error(f"Critical error: {e}")
        if args.verbosity == logging.DEBUG:
            import pdb, traceback

            extype, value, tb = sys.exc_info()
            traceback.print_exc()
            pdb.post_mortem(tb)
            raise
        return 1


def main():
    return main_(sys.argv[1:])
