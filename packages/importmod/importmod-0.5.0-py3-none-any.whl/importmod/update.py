# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import re
from typing import Dict, List, Optional
from urllib.parse import urlparse

from portmod.loader import load_all, load_pkg
from portmod.pybuild import Pybuild
from portmod.util import get_newest
from portmodlib.atom import Atom, version_gt
from portmodlib.usestr import use_reduce

from .sources import PackageSource, Update
from .sources.github import GithubSource
from .sources.gitlab import GitlabSource
from .sources.modhistory import ModhistorySource
from .sources.nexus import NexusSource, get_nexus_updates


def get_pkg_sources(mod: Pybuild) -> List[PackageSource]:
    sources: List[PackageSource] = []
    nexus_urls = []
    # FIXME: explicit metadata field for upstream sources
    if hasattr(mod, "NEXUS_URL"):
        nexus_urls = use_reduce(mod.NEXUS_URL, matchall=True, flat=True)
    else:
        # Check if HOMEPAGE contains a Nexus url
        for url in use_reduce(mod.HOMEPAGE, matchall=True, flat=True):
            hostname = urlparse(url).hostname
            if not hostname:
                continue
            if re.match(r"^\w*\.?nexusmods.com$", hostname):
                nexus_urls.append(url)
            elif re.match("^mw.modhistory.com$", hostname):
                modid = urlparse(url).path.split("-")[-1]
                sources.append(ModhistorySource(modid))
            elif re.match(r"^\w*\.?github.com$", hostname):
                basepath = "/".join(urlparse(url).path.lstrip("/").split("/")[:2])
                sources.append(GithubSource(basepath))
            elif re.match(r"^\w*\.?gitlab.com$", hostname):
                parsed = urlparse(url)
                basepath = "/".join(parsed.path.lstrip("/").split("/")[:2])
                sources.append(
                    GitlabSource(f"{parsed.scheme}://{parsed.netloc}", basepath)
                )

    for url in nexus_urls:
        game, modid = urlparse(url).path.split("/mods/")
        sources.append(NexusSource(game.lstrip("/"), int(modid)))

    return sources


def get_nexus_id_map() -> Dict[NexusSource, Pybuild]:
    """
    Returns a dictionary mapping NexusMod game,id to mod for all NexusMods in database
    """
    id_map: Dict[NexusSource, Pybuild] = {}
    for mod in load_all():
        ids = get_pkg_sources(mod)
        for modid in ids:
            if isinstance(modid, NexusSource):
                if modid in id_map:
                    if version_gt(mod.PV, id_map[modid].PV):
                        id_map[modid] = mod
                else:
                    id_map[modid] = mod
    return id_map


def get_updates(period: Optional[str] = None, repository: Optional[str] = None):
    """
    Returns a list of updates since the given time

    args:
        period: one of 1d, 1w, 1m
        repository: The path to the repository to process
                    only packages within this repository will be used
    """
    results: List[Update] = []
    if period:
        id_map = get_nexus_id_map()
        games = set(source.game for source in id_map)

        for game in games:
            results.extend(get_nexus_updates(game, period, id_map))
    else:
        pkgs = {
            get_newest(load_pkg(Atom(pkg.CPN)))
            for pkg in load_all(only_repo_root=repository)
        }
        for pkg in pkgs:
            print(f"Checking {pkg} for updates...")
            results += check_for_update(pkg)
    return results


def check_for_update(mod: Pybuild) -> List[Update]:
    updates = []

    for source in get_pkg_sources(mod):
        url = source.get_url()
        try:
            update = source.get_update(mod)
            if update:
                updates.append(update)
        except Exception as e:
            print(f"Unable to check {url}")
            print(e)
            updates.append(Update(oldatom=mod.ATOM, location=url))

    return updates
