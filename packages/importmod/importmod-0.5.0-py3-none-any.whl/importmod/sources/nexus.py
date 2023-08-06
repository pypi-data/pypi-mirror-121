# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""Utility functions for interacting with nexusmods.com"""

import json
import os
import urllib.parse
from collections import namedtuple
from datetime import datetime
from logging import warning
from typing import List, Optional, Tuple

import requests
from portmod.pybuild import Pybuild
from portmod.util import get_max_version
from portmodlib.atom import Atom, version_gt

from ..atom import parse_name, parse_version
from ..config import NEXUS_KEY
from . import PackageSource, Update

NexusData = namedtuple(
    "NexusData",
    [
        "atom",
        "modid",
        "name",
        "desc",
        "files",
        "homepage",
        "author",
        "nudity",
        "file_updates",
    ],
)


class APILimitExceeded(Exception):
    """Exception indicating that the NexusApi's daily limit has been exceeded"""


class NexusSource(PackageSource):
    def __init__(self, game: str, idnum: int):
        self.game = game
        self.idnum = idnum

    def get_newest_version(self) -> str:
        nexus_info = get_nexus_info(self.game, self.idnum)
        return parse_version(nexus_info.atom.PV)

    def get_url(self) -> str:
        return f"https://www.nexusmods.com/{self.game}/mods/{self.idnum}"

    def __hash__(self):
        return hash((self.game, self.idnum))

    def get_update(self, pkg: Pybuild) -> Optional[Update]:
        nexus_info = get_nexus_info(self.game, self.idnum)
        newest = parse_version(nexus_info.atom.PV)
        if version_gt(newest, pkg.PV):
            print(f"Found update for {pkg}. New version: {newest}")
            return Update(
                oldatom=pkg.ATOM,
                newatom=Atom(f"{pkg.CPN}-{newest}"),
                location=self.get_url(),
            )

        manifest = pkg.get_manifest()
        for update in nexus_info.file_updates:
            old_file_name = update["old_file_name"]
            new_file_name = update["new_file_name"]
            time = datetime.fromisoformat(update["uploaded_time"])
            if manifest.get(old_file_name.replace(" ", "_")):
                # Ignore file changes older than the package file
                if os.path.getmtime(pkg.FILE) < time.timestamp():
                    return Update(
                        oldatom=pkg.ATOM,
                        title=f"[{pkg.CPN}] File has been changed without a version bump",
                        description=f"File {old_file_name} was replaced by {new_file_name} on {time}",
                        location=self.get_url(),
                    )

        return None


def parse_nexus_url(url: str) -> Tuple[str, int]:
    parsed = urllib.parse.urlparse(url)
    game = parsed.path.split("/")[1]
    mod_id = int(parsed.path.split("/")[3])
    return game, mod_id


def get_nexus_info(game: str, modid: int) -> NexusData:
    """
    Fetches mod information from nexusmods.com and parses it into a NexusData object
    """
    info_url = f"https://api.nexusmods.com/v1/games/{game}/mods/{modid}/"
    files_url = f"https://api.nexusmods.com/v1/games/{game}/mods/{modid}/files/"

    headers = {"APIKEY": NEXUS_KEY, "content-type": "application/json"}

    rinfo = requests.get(info_url, headers=headers)
    if rinfo.headers.get("X-RL-Daily-Remaining") == 0:
        raise APILimitExceeded()

    rfiles = requests.get(files_url, headers=headers)

    if (
        rinfo.status_code
        == rfiles.status_code
        == requests.codes.ok  # pylint: disable=no-member
    ):
        info = json.loads(rinfo.text)
        files = json.loads(rfiles.text)
    else:
        rinfo.raise_for_status()
        rfiles.raise_for_status()

    version = parse_version(info["version"]) or "0.1"

    # Select all files except those in the OLD_VERSION category
    tmpfiles = [
        file
        for file in files["files"]
        if file["category_name"] != "OLD_VERSION" and file["category_name"]
    ]

    allversions = [version]
    for file in tmpfiles:
        tmp_ver = parse_version(file["version"])
        if tmp_ver:
            allversions.append(tmp_ver)

    # Mod author may not have updated the mod version.
    # Version used should be the newest file version among the files we selected
    version = get_max_version(allversions)

    atom = Atom(parse_name(info["name"]) + "-" + version)

    files_list = []
    for file in tmpfiles:
        skip = False

        # Ignore exe files. We can't use them anyway
        _, ext = os.path.splitext(file["file_name"])
        if ext == ".exe":
            skip = True

        if not skip:
            files_list.append(file)

    return NexusData(
        atom=Atom(atom),
        modid=modid,
        name=info["name"],
        desc=info["summary"].replace("\\", ""),
        files={file["file_name"].replace(" ", "_"): file for file in files_list},
        homepage=f"https://www.nexusmods.com/{game}/mods/{modid}",
        author=info["author"],
        nudity=info["contains_adult_content"],
        file_updates=files["file_updates"],
    )


def validate_file(game, mod_id, file, hash):
    hash_url = f"https://api.nexusmods.com/v1/games/{game}/mods/md5_search/{hash}.json"

    headers = {"APIKEY": NEXUS_KEY, "content-type": "application/json"}

    response = requests.get(hash_url, headers=headers)

    if response.status_code == requests.codes.not_found:  # pylint: disable=no-member
        return False

    mods = json.loads(response.text)
    for mod in mods:
        if mod["mod"]["mod_id"] == mod_id:
            return True

    modnames = [mod.get("mod").get("name") for mod in mods]
    if all(mod.get("mod").get("status") == "hidden" for mod in mods):
        warning("Hidden mods matched the file!")
        return True
    Exception(f"Invalid response {modnames} from NexusMods API when hashing {file}")


def get_nexus_updates(game: str, period: str, mod_map) -> List[Update]:
    """
    Returns a list of updates to nexusmods.com mods in the given period

    Valid periods are 1d, 1w, 1m
    """
    assert period in ["1d", "1w", "1m"]
    update_url = (
        f"https://api.nexusmods.com/v1/games/{game}/mods/updated.json?period={period}"
    )

    headers = {"APIKEY": NEXUS_KEY, "content-type": "application/json"}

    uinfo = requests.get(update_url, headers=headers)
    if uinfo.headers["X-RL-Daily-Remaining"] == 0:
        raise APILimitExceeded()

    if uinfo.status_code == requests.codes.ok:  # pylint: disable=no-member
        info = json.loads(uinfo.text)
    else:
        uinfo.raise_for_status()

    updates = []
    for mod in info:
        source = NexusSource(game, mod["mod_id"])
        if source in mod_map:
            update = source.get_update(mod_map[source])
            if update:
                updates.append(update)
    return updates
