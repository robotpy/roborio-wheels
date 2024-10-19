#!/usr/bin/env python3

import argparse
import glob
import os
import sys
import subprocess
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

    env = os.environ.copy()
    env["PATH"] = f"{env['PATH']}:/build/venv/build/bin"
    if "environment" in pkgdata:
        env.update(pkgdata["environment"])

    pipargs = [
        sys.executable,
        "-m",
        "pip",
        "--disable-pip-version-check",
        "-v",
        "wheel",
        "--no-build-isolation",
        "--no-deps",
        "--no-binary",
        ":all:",
        "-w",
        "dist",
        f"{args.project}=={version}",
    ]
    result = subprocess.run(pipargs, env=env)

    # Sets variable for use in github actions
    if result.returncode == 0:
        project_cvt = args.project.replace("-", "_")
        for f in glob.glob(f"dist/{project_cvt}-{version}-*.whl"):
            print(f"::set-output name=wheel::{f}")

    exit(result.returncode)
