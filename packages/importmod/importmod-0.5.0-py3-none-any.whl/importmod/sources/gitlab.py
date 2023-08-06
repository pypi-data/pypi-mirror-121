# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""Utility functions for interacting with Github"""

from gitlab import Gitlab

from ..atom import parse_version
from . import PackageSource


class GitlabSource(PackageSource):
    def __init__(self, server: str, identifier: str):
        self.server = server
        self.id = identifier

    def get_newest_version(self):
        gl = Gitlab(self.server)
        repo = gl.projects.get(self.id)
        releases = repo.releases.list()
        if releases:
            tag = releases[0].tag_name
            return parse_version(tag)

        return "0"

    def get_url(self) -> str:
        return f"{self.server}/{self.id}"

    def __hash__(self):
        return hash((self.server, self.id))
