#!/usr/bin/env python

# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

from setuptools import find_packages, setup

setup(
    name="importmod",
    author="Portmod Authors",
    description="A CLI tool to import mods into the Portmod repository format",
    license="GPLv3",
    url="https://gitlab.com/portmod/importmod",
    packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "test"]),
    entry_points=({"console_scripts": ["importmod = importmod.main:main"]}),
    install_requires=[
        "portmod>=2.0rc10",
        "gitpython",
        "requests",
        "patool",
        "redbaron",
        "isort>=5.0.0",
        "black",
        "beautifulsoup4",
        "pygithub",
        "python-gitlab",
    ],
    setup_requires=["setuptools_scm"],
    python_requires=">=3.7",
    use_scm_version=True,
)
