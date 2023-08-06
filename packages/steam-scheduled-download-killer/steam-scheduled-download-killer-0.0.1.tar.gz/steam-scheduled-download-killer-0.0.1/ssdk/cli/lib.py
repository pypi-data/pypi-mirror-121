##
#   Copyright (c) 2021 Valentin Weber
#
#   This file is part of the software steam-scheduled-download-killer.
#
#   The software is licensed under the European Union Public License
#   (EUPL) version 1.2 or later. You should have received a copy of
#   the english license text with the software. For your rights and
#   obligations under this license refer to the file LICENSE or visit
#   https://joinup.ec.europa.eu/community/eupl/og_page/eupl to view
#   official translations of the licence in another language of the EU.
##

"""Parser and entry point for ssdk-lib."""

import argparse
import sys

from . import SSDK_MAIN, SSDK_LIB
from ..config import Config, ConfigFileError
from ..core.utils import BaseArgumentParser


class SsdkLibParser(BaseArgumentParser):
    """Command Line Parser for ssdk-lib entry point."""

    ALLOWED_COMMANDS = {
        "make": "create a config file with all given Steam Library Folder(s)",
        "list": "show a list of all Steam Library Folder(s)",
        "rm": "remove the given Steam Library Folder(s) from config file",
        "add": "add given Steam Library Folder(s) to config file"
    }

    def __init__(self):
        """Initialize the parser and add arguments."""
        desc = (
            "Manage file listing Steam Library Folders.\n"
            f"Use '{SSDK_MAIN}' entry point for managing Steam Applications."
        )
        super().__init__(
            prog=SSDK_LIB,
            desc=desc,
            epilog=self.get_epilog(),
        )
        self.add_argument(
            "--ignore-existing",
            help="set this to overwrite existing file for 'make' command",
            action="store_true",
            dest="ignore"
        )
        self.add_argument(
            "command",
            metavar="COMMAND",
            help="action to be executed (see allowed commands for details)",
            choices=self.ALLOWED_COMMANDS.keys(),
        )
        self.add_argument(
            "libraries",
            metavar="LIBRARY",
            help="path(s) to Steam Library Folders (not needed for 'list')",
            nargs="*"
        )

    def get_epilog(self) -> str:
        """Create formatted help message for each allowed command."""
        help_messages = (
            f"  {cmd:28}{msg}" for cmd, msg in self.ALLOWED_COMMANDS.items()
        )
        return "allowed commands:\n" + "\n".join(help_messages)

    def get_validated_args(self) -> argparse.Namespace:
        """Parse and validate the command line arguments."""
        args = self.parse_args()
        if args.command != "list" and not args.libraries:
            self.error(
                "the following arguments are required for command"
                f" '{args.command}': LIBRARY"
            )
        return args


def main() -> None:
    """ssdk-lib entry point."""
    cli = SsdkLibParser()
    args = cli.get_validated_args()
    cfg = Config(args.config)
    try:
        if (cmd := args.command) == "add":
            cfg.add(args.libraries)
        elif cmd == "rm":
            cfg.remove(args.libraries)
        elif cmd == "make":
            cfg.write(args.libraries, args.ignore)
        elif cmd == "list":
            print("\n".join(str(lib) for lib in cfg.read()))
    except ConfigFileError as exc:
        print("ERROR: " + exc.args[0])
        sys.exit(1)
    except KeyboardInterrupt:
        print("Exiting Application.")
        sys.exit(99)
    except:  # noqa pylint: disable=bare-except
        print("ERROR: caught an unexpected exception")
        sys.exit(2)


if __name__ == '__main__':
    main()
