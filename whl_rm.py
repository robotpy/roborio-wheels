#!/usr/bin/env python3
#
# Removes non-matching wheels
#

import argparse
import os.path
import pathlib
import tomllib


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("project")
    parser.add_argument("--config", default="packages.toml")

    args = parser.parse_args()

    with open(args.config, "rb") as fp:
        cfg = tomllib.load(fp)

    try:
        pkgdata = cfg["packages"][args.project]
        version = pkgdata["version"]
    except KeyError:
        parser.error(f"{args.project} not found in {args.config}")

    project = pkgdata.get("name", args.project)

    for f in pathlib.Path("dist").iterdir():
        if f.is_file() and not f.match(f"{project}*.whl"):
            print("DELETE", f)
            # f.unlink()
