from __future__ import annotations
from typing import *
import argparse
from pathlib import Path
import os
from textwrap import dedent

from rich.console import Console

from argcomplete import autocomplete

from . import io, dyn, err, log as logging
from .rich_fmt import RichFormatter


class HelpErrorView(io.ErrorView):
    def render_rich(self):
        io.render_to_console(self.data.format_rich_help())

    def render_json(self):
        raise err.UserError("Help not available as JSON")


class _SubParsersAction(argparse._SubParsersAction):
    """\
    Extended to use help as description if the later is missing.
    """

    def add_parser(self, name, **kwds):
        if "help" in kwds and "description" not in kwds:
            kwds["description"] = kwds["help"]
        return super().add_parser(name, **kwds)


class ArgumentParser(argparse.ArgumentParser):
    @classmethod
    def create(cls, description, subparser_hook):
        if isinstance(description, Path):
            with description.open("r") as file:
                description = file.read()
        elif isinstance(description, str):
            pass
        else:
            raise TypeError("Expected `pathlib.Path` or `str`")

        parser = cls(
            description=description,
            notes=dedent(
                """\
                You can run

                    eval "$(register-python-argcomplete %(prog)s)"

                in your bash shell to enable tab-completion.
                """
            ),
        )

        subparsers = parser.add_subparsers(help="Select a command")
        subparser_hook(subparsers)
        autocomplete(parser)
        return parser

    def __init__(self, *args, target=None, view=io.View, notes=None, **kwds):
        super().__init__(*args, formatter_class=RichFormatter, **kwds)

        self.notes = notes
        self.register("action", "parsers", _SubParsersAction)

        if target is None:
            self.set_target(self.no_target)
        else:
            self.set_target(target)

        self.add_argument(
            "-B",
            "--backtrace",
            action="store_true",
            help="Print backtraces on error",
        )

        # self.add_argument(
        #     '--log',
        #     type=str,
        #     help="File path to write logs to.",
        # )

        self.add_argument(
            "-V",
            "--verbose",
            action="count",
            help="Make noise.",
        )

        self.add_argument(
            "-O",
            "--output",
            default=view.DEFAULT_FORMAT,
            help=view.help(),
        )

    def no_target(self):
        return HelpErrorView(self)

    def env_var_name(self, name):
        return self.prog.upper() + "_" + name.upper()

    def env(self, name, default=None):
        return os.environ.get(self.env_var_name(name), default)

    def is_backtracing(self, pkg_name, args):
        return (
            args.backtrace
            or logging.get_pkg_logger(pkg_name).level is logging.DEBUG
            or self.env("backtrace", False)
        )

    def set_target(self, target):
        self.set_defaults(__target__=target)

    def action_dests(self):
        return [
            action.dest
            for action in self._actions
            if action.dest != argparse.SUPPRESS
        ]

    def add_children(self, module__name__, module__path__):
        subparsers = self.add_subparsers()

        for module in dyn.children_modules(module__name__, module__path__):
            if hasattr(module, "add_to"):
                module.add_to(subparsers)

    def format_rich_help(self):
        formatter = self._get_formatter()

        # usage
        formatter.add_usage(
            self.usage, self._actions, self._mutually_exclusive_groups
        )

        # description
        formatter.start_section("description")
        formatter.add_text(self.description)
        formatter.end_section()

        # positionals, optionals and user-defined groups
        for action_group in self._action_groups:
            formatter.start_section(action_group.title)
            formatter.add_text(action_group.description)
            formatter.add_arguments(action_group._group_actions)
            formatter.end_section()

        if self.notes is not None:
            formatter.start_section("additional notes")
            formatter.add_text(self.notes)
            formatter.end_section()

        # epilog
        formatter.add_text(self.epilog)

        # determine help from format above
        return formatter.format_rich()

    def format_help(self) -> str:
        return io.render_to_string(self.format_rich_help())

    def print_help(self, file=None):
        if file is None:
            console = io.OUT
        elif isinstance(file, Console):
            console = file
        else:
            console = Console(file=file)
        console.print(self.format_rich_help())
