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

"""Parser and entry point for ssdk."""

import sys

from . import SSDK_MAIN, SSDK_LIB
from ..config import Config, ConfigFileError
from ..manifest import ManifestFileError, ManifestHandler, ManifestKeyError
from ..core.utils import BaseArgumentParser


class SsdkParser(BaseArgumentParser):
    """Command Line Parser for ssdk entry point."""

    ALLOWED_PRIORITIES = {
        "0": "always keep this game updated",
        "1": "only update this game when I launch it",
        "2": "high priority - always auto-update this game before others"
    }

    def __init__(self):
        """Initialize the parser and add arguments."""
        desc = (
            "Ensure all Steam Games have high priority auto updates.\n"
            f"Manage Steam Library Folder(s) with entry point '{SSDK_LIB}'"
        )
        super().__init__(SSDK_MAIN, desc, self.get_epilog())

        self.add_argument(
            "--update-priority",
            help="value the update priority should be set to (default: 2)",
            type=int,
            choices=range(3),
            default=2,
            metavar="PRIO"
        )

    def get_epilog(self) -> str:
        """Create formatted help message for each priority value."""
        help_messages = (
            f"  {cmd:28}{msg}" for cmd, msg in self.ALLOWED_PRIORITIES.items()
        )
        return "priority values:\n" + "\n".join(help_messages)


def main() -> None:
    """Run entry point ssdk."""
    cli = SsdkParser()
    args = cli.parse_args()
    try:
        libraries = Config(args.config).read()
    except ConfigFileError as exc:
        print("ERROR:", exc.args[0])
        sys.exit(1)
    update_count = 0
    for lib in libraries:
        try:
            manifest_files = lib.get_appmanifest_list()
        except OSError:
            print(f"ERROR: unable to fetch manifests in '{lib.path}'")
            continue
        print(f"=== Steam Library: {lib}")
        for manifest_path in manifest_files:
            try:
                manifest = ManifestHandler(manifest_path)
                if manifest.update_priority == args.update_priority:
                    print(f"    Skipped '{manifest.game_title}'")
                else:
                    manifest.write_new_update_priority(args.update_priority)
                    print(f"    Updated '{manifest.game_title}'")
                    update_count += 1
            except ManifestFileError as exc:
                print("    ERROR:", ": ".join(exc.args))
            except ManifestKeyError:
                print("    ERROR: unable to parse manifest file content")
    exit_msg = f"Updated {update_count} games in {len(libraries)} libraries."
    if update_count > 0:
        exit_msg += " Restart Steam for changes to take effect."
    print(exit_msg)


if __name__ == '__main__':
    main()
