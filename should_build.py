#!/usr/bin/env python3
#
# Helper for github actions, intended to be ran in the cross-compilation
# environment
#

import argparse
from html.parser import HTMLParser
import posixpath
import subprocess
import sys
import typing
from urllib.parse import unquote_plus
from urllib.request import urlopen

from packaging.tags import parse_tag, sys_tags
import toml

# https://www.mschweighauser.com/fast-url-parsing-with-python/
class LinkFinder(HTMLParser):
    @classmethod
    def extract_links(cls, content: str) -> typing.List[str]:
        parser = cls()
        parser.feed(content)
        return parser.links

    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if "href" in attr[0]:
                    self.links.append(attr[1])
                    return


def find_wheel_url(project: str, version: str, content: str):

    project = project.replace("-", "_")
    tags = set(sys_tags())

    links = LinkFinder.extract_links(content)
    not_matched = []
    found = False

    for link in links:
        link = posixpath.basename(unquote_plus(link))
        if not link.endswith(".whl"):
            continue

        wproject, wversion, wtags = link[:-4].split("-", 2)
        if wproject != project:
            continue

        # Add to list so we can print it at the end if nothing matches
        not_matched.append(link)

        if wversion != version:
            continue

        for wtag in parse_tag(wtags):
            if wtag in tags:
                print("Found matching wheel", link)
                return True

    if not found:
        print("Did not find matching wheels in:")
        for link in not_matched:
            print("-", link)

    return False


def get_find_links() -> str:
    """
    Retrieves --find-links setting for pip
    """
    content = subprocess.check_output(
        ["pip", "--disable-pip-version-check", "config", "list"], encoding="utf-8"
    )
    for line in content.splitlines():
        s = line.split("global.find-links=", 1)
        if len(s) == 2:
            return s[1].strip("'")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("project")
    parser.add_argument("--config", default="packages.toml")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--url", default=None)
    group.add_argument("-f", "--file", default=None)

    args = parser.parse_args()

    with open(args.config) as fp:
        cfg = toml.load(fp)
    
    try:
        version = cfg["packages"][args.project]["version"]
    except KeyError:
        parser.error(f"{args.project} not found in {args.config}")

    if args.file:
        with open(args.file) as fp:
            content = fp.read()
    else:
        url = args.url
        if not url:
            url = get_find_links()

        if not url:
            parser.error("URL to parse must be specified!")

        print("Checking", url)
        with urlopen(url) as f:
            content = f.read().decode("utf-8")

    found = find_wheel_url(args.project, version, content)

    # Sets variable for use in github actions
    print(f"::set-output should_build={str(not found).lower()}")
