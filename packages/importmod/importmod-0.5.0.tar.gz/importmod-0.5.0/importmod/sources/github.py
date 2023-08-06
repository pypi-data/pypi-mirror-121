# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""Utility functions for interacting with Github"""

from github import Github

from ..atom import parse_version
from . import PackageSource


class GithubSource(PackageSource):
    def __init__(self, identifier: str):
        self.id = identifier

    def get_newest_version(self):
        gh = Github()
        repo = gh.get_repo(self.id)
        releases = repo.get_releases()
        if releases and releases.totalCount > 0:
            return parse_version(releases[0].tag_name)
        else:
            return "0"

    def get_url(self) -> str:
        return f"https://github.com/{self.id}"

    def __hash__(self):
        return hash(self.id)
