#
# file setup.py
#
# SPDX-FileCopyrightText: (c) 2022 Michal Kielan
#
# SPDX-License-Identifier: GPL-3.0-only
#

from setuptools import setup, find_packages

setup(
    name="fzcat",
    version="0.1.0",
    description="Tool to sort and print logs from logcat file.",
    author="Michal Kielan",
    author_email="michalkielan@protonmail.com",
    packages=find_packages(exclude=("tests", "docs")),
    entry_points={"console_scripts": ["fzcat = fzcat.fzcat:main"]},
    python_requires=">3.6.0",
    test_suite="tests",
)
