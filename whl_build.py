#!/usr/bin/env python3

import argparse
import os
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
        version = pkgdata["version"]
    except KeyError:
        parser.error(f"{args.project} not found in {args.config}")

    env = None
    if "environment" in pkgdata:
        env = os.environ.copy()
        env.update(pkgdata["environment"])

    pipargs = [
        sys.executable,
        "-m",
        "pip",
        "--disable-pip-version-check",
        "-v",
        "wheel",
        "-w",
        "dist",
        f"{args.project}=={version}",
    ]
    result = subprocess.run(pipargs, env=env)
    exit(result.returncode)
