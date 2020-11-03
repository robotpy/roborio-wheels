#!/usr/bin/env python3
#
# Modifies a wheel to have different installation requirements
#

import argparse
import os.path
import sys
import subprocess
import toml
import tempfile
import typing


def add_requirements_to_wheel(
    wheel: str, project: str, version: str, reqs: typing.List[str]
):
    whldir = os.path.dirname(wheel)
    if whldir == "":
        whldir = "."

    with tempfile.TemporaryDirectory() as tmpdir:
        # unpack the wheel
        args = [sys.executable, "-m", "wheel", "unpack", "-d", tmpdir, wheel]
        subprocess.check_call(args)

        unpacked_root = os.path.join(tmpdir, f"{project}-{version}")

        # Find and modify the metadata record
        metadata_path = os.path.join(
            unpacked_root, f"{project}-{version}.dist-info", "METADATA"
        )
        with open(metadata_path, "r+") as fp:
            lines = fp.readlines()

            # Find the first empty line and insert our extra requirements there
            i = 0
            for i, line in enumerate(lines):
                if line.strip() == "":
                    break

            for req in reversed(reqs):
                lines.insert(i, f"Requires-Dist: {req}\n")

            print("-" * 72)
            for line in lines:
                print(line.strip())
            print("-" * 72)

            fp.seek(0)
            fp.writelines(lines)
            fp.truncate()

        # pack the wheel back up
        args = [sys.executable, "-m", "wheel", "pack", unpacked_root, "-d", whldir]
        subprocess.check_call(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("wheel")
    parser.add_argument("--config", default="packages.toml")

    args = parser.parse_args()

    with open(args.config) as fp:
        cfg = toml.load(fp)

    project, _ = os.path.basename(args.wheel).split("-", 1)

    try:
        pkgdata = cfg["packages"][project]
        version = pkgdata["version"]
    except KeyError:
        parser.error(f"{project} not found in {args.config}")

    reqs = pkgdata.get("install_requirements")
    if reqs:
        add_requirements_to_wheel(args.wheel, project, version, reqs)
