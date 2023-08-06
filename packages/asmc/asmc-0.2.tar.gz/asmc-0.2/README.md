# ASMC python umbrella

A Python module that contains no functionality but provides the following dependencies:

- [ASMC](https://pypi.org/project/asmc-asmc/)
- [PrepareDecoding](https://pypi.org/project/asmc-preparedecoding/)

This module is intended for someone to obtain all related ASMC python tools by doing:

```bash
pip install asmc
```

When new release of this module is made on GitHub a workflow should automatically publish new wheels to PyPI.

:warning: **New wheels cannot be published until Fergus has access to ASMC on PyPI** :warning:

## Making a new release

**Increment version numbers**

- Bump `version` in [setup.cfg](./setup.cfg)
- Bump `install_requires` dependency versions in [setup.cfg](./setup.cfg)
- Bump version numbers stated in [README_PyPI.md](./README_PyPI.md)

**Make a release on GitHub**

- Commit and push the changes above
- Create a new tag (with the new version number for the umbrella)
- Create a release on GitHub

Then just check that the new version has appeared on PyPI a few minutes later.
