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

"""Utilities for steam-scheduled-download-killer."""

import argparse
import os


class BaseArgumentParser(argparse.ArgumentParser):
    """Command Line Parser with attribute for config file."""

    def __init__(self, prog: str, desc: str, epilog: str):
        """Initialize the argparse.Argumentparser and add arguments."""
        super().__init__(
            prog=prog,
            description=desc,
            epilog=epilog,
            formatter_class=OneLineHelpFormatter
        )
        self.add_argument(
            "-c", "--config",
            help="path to config file containing Steam Library Folder(s)",
            default=os.path.expanduser(r"~\AppData\Local\python-ssdk\ssdk.cfg")
        )


class OneLineHelpFormatter(argparse.RawTextHelpFormatter):
    """Extension for argparse.RawTextHelpFormatter."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize RawTextHelpFormatter with greater line length."""
        super().__init__(*args, **kwargs)
        self._max_help_position = 999


def get_abspath(path: str) -> str:
    """Return normalized absolute version of given path."""
    if not os.path.isabs(path):
        if path.startswith("~"):
            path = os.path.expanduser(path)
        else:
            path = os.path.abspath(path)
    return os.path.normpath(path)
