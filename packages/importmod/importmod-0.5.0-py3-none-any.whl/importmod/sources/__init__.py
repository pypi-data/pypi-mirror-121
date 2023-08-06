# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

from abc import ABC, abstractmethod
from typing import Optional

from portmod.pybuild import Pybuild
from portmod.util import get_max_version
from portmodlib.atom import Atom

"""Upstream mod repositories"""


class Update:
    def __init__(
        self,
        *,
        oldatom: Atom,
        location: str,
        newatom: Optional[Atom] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ):
        self.oldatom = oldatom
        self.newatom = newatom
        self.location = location
        self.available = newatom is not None

        if not title and not description:
            if newatom is not None:
                self.title = f"[{oldatom.CPN}] Version {newatom.PV} is available"
                self.description = (
                    f"Old Version: {oldatom}\\\n"
                    f"New Version: {oldatom.CPN}-{newatom.PVR}\n\n"
                    f"New version can be found here: {location}\n\n"
                    "*Note: this is an automatically generated message. "
                    "Please report any issues [here]"
                    "(https://gitlab.com/portmod/importmod/issues)*"
                )
            else:
                self.title = (
                    f"[{oldatom.CPN}] Mod is no longer available from current source"
                )
                self.description = (
                    f"Attempt to check mod availability from: {location} failed.\n\n"
                    "*Note: this is an automatically generated message. "
                    "Please report any issues [here]"
                    "(https://gitlab.com/portmod/importmod/issues)*"
                )
        else:
            assert title
            assert description
            self.title = title
            self.description = description


class PackageSource(ABC):
    @abstractmethod
    def get_newest_version(self) -> str:
        """Returns the newest release version for this source"""

    @abstractmethod
    def get_url(self) -> str:
        """Returns the URL associated with this source"""

    def get_update(self, pkg: Pybuild) -> Optional[Update]:
        newest = self.get_newest_version()
        if newest != pkg.PV and get_max_version([newest, pkg.PV]) == newest:
            print(f"Found update for {pkg}. New version: {newest}")
            return Update(
                oldatom=pkg.ATOM,
                newatom=Atom(f"{pkg.CPN}-{newest}"),
                location=self.get_url(),
            )

        return None
