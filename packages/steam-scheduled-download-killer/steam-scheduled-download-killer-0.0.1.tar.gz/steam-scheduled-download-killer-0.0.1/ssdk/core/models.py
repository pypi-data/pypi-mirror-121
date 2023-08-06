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

"""Data Models for steam-scheduled-download-killer."""

from dataclasses import dataclass
import os
from typing import List


@dataclass(repr=True)
class SteamLibrary:
    """Container for a Steam Library."""

    path: str

    def get_appmanifest_list(self) -> List[str]:
        """List all appmanifest.acf files in Steam Library Folder."""
        manifests = [
            os.path.join(self.path, man) for man in os.listdir(self.path)
            if os.path.isfile(os.path.join(self.path, man))
            and man.startswith("appmanifest_") and man.endswith(".acf")
        ]
        return manifests

    @property
    def game_count(self) -> int:
        """Return number of games found in Steam Library Folder."""
        return len(self.get_appmanifest_list())

    def __str__(self) -> str:
        """Return string with library path and number of manifests."""
        return f"{self.path} (found {self.game_count} games)"
