# StatGenTools

A Python module that contains no functionality but will later provide the dependencies such as ASMC.

When new release of this module is made on GitHub a workflow should automatically publish new wheels to PyPI.

## Making a new release

**Increment version numbers**

- Bump `version` in [setup.cfg](./setup.cfg)

**Make a release on GitHub**

- Commit and push the changes above
- Create a new tag (with the new version number for the umbrella)
- Create a release on GitHub

Then just check that the new version has appeared on PyPI a few minutes later.
