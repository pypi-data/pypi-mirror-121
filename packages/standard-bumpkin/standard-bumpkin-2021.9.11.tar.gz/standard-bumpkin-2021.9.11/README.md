
[![PyPI](https://img.shields.io/pypi/v/standard-bumpkin)](https://pypi.org/project/standard-bumpkin/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/standard-bumpkin)](https://pypi.org/project/standard-bumpkin/)
 [![codecov](https://codecov.io/gh/fredheidrich/bumpkin/branch/main/graph/badge.svg?token=WCM92TNZCA)](https://codecov.io/gh/fredheidrich/bumpkin)

# Standard Bumpkin

```bash
pip install standard-bumpkin
```

# Usage

```bash
git config --global user.email "foo@bar.com"
git config --global user.name "Autoversion"
bumpkin --help
```

```bash
# output commands to run without performing them
bumpkin --dry-run

# bump and push version if commits matching the tag specs are found
bumpkin
```

```bash
# bump and push version regardless, as long as there are new commits since the last tag
bumpkin --force

# bump version without generating a changelog or version file, just a tag
bumpkin --no-changelog --no-version-file --force
```

# What is it?

A utility that parses git commit history, formulates a changelog and creates a git release. It currently only does one thing and contain plenty of bugs. Use at your own risk.
