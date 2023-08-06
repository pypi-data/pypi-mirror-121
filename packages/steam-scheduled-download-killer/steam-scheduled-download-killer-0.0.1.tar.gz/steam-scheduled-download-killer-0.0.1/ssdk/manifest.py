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

"""Main functionality for Steam appmanifest.acf file interaction."""

import re

from typing import IO, Tuple


class ManifestFileError(Exception):
    """Exception for errors during manifest file interaction."""


class ManifestKeyError(Exception):
    """Exception for errors during parsing manifest keys and values."""


class ManifestHandler:
    """Handler for interacting with appmanifest.acf files."""

    def __init__(self, path: str) -> None:
        """Initialize handler for given manifest file."""
        self.file = path
        self.raw_content = self.get_raw_content()
        self.priority_key, self.update_priority = self.parse_update_priority()

    def get_raw_content(self) -> str:
        """Return string of appmanifest content without processing."""
        with self._open() as manifest:
            return manifest.read()

    def parse_update_priority(self) -> Tuple[re.Match, int]:
        """Get match obj & value for manifest key AutoUpdateBehavior."""
        search = re.search(  # Example Entry: '\t"AutoUpdateBehavior"\t\t"0"'
            r'\t"AutoUpdateBehavior"\t\t"(\d)"', self.raw_content
        )
        if search is None:
            raise ManifestKeyError("AutoUpdateBehavior")
        return search, int(search.group(1))

    def write_new_update_priority(self, priority: int = 2) -> None:
        """Write new value for AutoUpdateBehavior key to appmanifest."""
        key_str = self.priority_key.group()
        new_content = self.raw_content.replace(
            key_str, key_str.replace(str(self.update_priority), str(priority))
        )
        with self._open("w") as manifest:
            manifest.write(new_content)

    @property
    def game_title(self) -> str:
        """Extract title of game from manifest contents."""
        search = re.search(r'\t"name"\t\t"(.*)"', self.raw_content)
        if search is None:
            raise ManifestKeyError("name")
        return search.group(1)

    def _open(self, filemode="r") -> IO:
        """Open manifest file in specified mode."""
        try:
            return open(self.file, filemode, encoding="utf-8")
        except OSError as exc:
            raise ManifestFileError(
                "cannot access manifest file", self.file
            ) from exc


if __name__ == '__main__':
    test_manifest = ManifestHandler(r".test_manifests\appmanifest_261640.acf")
    print(
        test_manifest.game_title,
        test_manifest.priority_key,
        test_manifest.update_priority,
        sep="\n", end="\n"
    )
