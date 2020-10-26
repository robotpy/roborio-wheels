roborio-wheels
==============

This repository exists to build binary wheels of non-RobotPy software for use
on the roborio.

When you make a pull request to this repo, a github action is automatically
triggered and will upload any new artifacts to the github action so that 
you can download and use them. Once merged to master, the built artifacts
will be uploaded for all teams to use.

Adding a new build
------------------

First, add a section to `packages.toml`, similar to this:

```
[packages.pydevd]
version = "2.0.0"
```

Second, edit `.github/workflows/wheels.yml` and add the package to the `package`
list under 'matrix'.

Finally, commit your changes and make a pull request


Updating the version of a build
-------------------------------

Edit the version in `packages.toml` and make a pull request.

