#!/usr/bin/env python3
#
# Installs extra requirements

import argparse
import sys
import subprocess
import toml


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("project")
    parser.add_argument("--config", default="packages.toml")

    args = parser.parse_args()

    with open(args.config) as fp:
        cfg = toml.load(fp)

    try:
        pkgdata = cfg["packages"][args.project]
    except KeyError:
        parser.error(f"{args.project} not found in {args.config}")

    if "build_requirements" in pkgdata:
        pipargs = [
            sys.executable,
            "-m",
            "pip",
            "--disable-pip-version-check",
            "install",
        ]
        pipargs.extend(pkgdata["build_requirements"])
        subprocess.check_call(pipargs)