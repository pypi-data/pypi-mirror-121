# Version helper

`version-helper` is a package for a better version management in python projects.

_This package is still under development. Code may change frequently._

[![PyPI](https://img.shields.io/pypi/v/version-helper)][version-helper-pypi]
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/version-helper)][version-helper-pypi]
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/version-helper)][version-helper-pypi]
[![codecov](https://codecov.io/gh/dl6nm/version-helper/branch/main/graph/badge.svg?token=WNOMQ28E5J)](https://codecov.io/gh/dl6nm/version-helper)
[![main](https://github.com/dl6nm/version-helper/actions/workflows/main.yml/badge.svg)](https://github.com/dl6nm/version-helper/actions/workflows/workflow.yml)
[![Lines of code](https://img.shields.io/tokei/lines/github/dl6nm/version-helper)][version-helper-github]
[![GitHub](https://img.shields.io/github/license/dl6nm/version-helper)](https://github.com/dl6nm/version-helper/blob/main/LICENSE.md)

    from version_helper import Version
    v = Version.get_from_git_describe()
    print(v.core)  # major.minor.patch
    print(v.full)  # major.minor.patch[-prerelease][+build]

## Table of contents

- [Version helper](#version-helper)
    - [Table of contents](#table-of-contents)
    - [Requirements](#requirements)
    - [Installing `version-helper`](#installing-version-helper)
    - [Usage](#usage)
        - [Reading version from a file](#reading-version-from-a-file)
        - [Writing version to a file](#writing-version-to-a-file)
    - [Changelog](#changelog)
    - [References](#references)

## Requirements

- [Python][python] 3.6+
- [Git][git], if you'd need to receive a version string from `git describe`

## Installing `version-helper`

    pip install version-helper

## Usage

### Reading version from a file

    import pathlib
    from version_helper import Version
    
    version = Version.read_from_file(
        file=pathlib.Path('/path/to/my/version_file.txt'),
        variable_name='APP_VERSION',
        separator='=',
    )
    print(version)

### Writing version to a file

    import pathlib
    from version_helper import Version
    
    version = Version(1, 2, 3)
    version.write_to_file(
        file=pathlib.Path('/path/to/my/version_file.txt'),
        variable_name='APP_VERSION',
        separator='=',
    )

## Changelog

All notable changes to this project will be documented in the [CHANGELOG.md](CHANGELOG.md).

## References

- [git-describe](https://git-scm.com/docs/git-describe)
- [Poetry](https://python-poetry.org/)
- [Semantic Versioning](https://semver.org/)



[git]: https://git-scm.com/
[python]: https://www.python.org/

[version-helper-github]: https://github.com/dl6nm/version-helper/
[version-helper-pypi]: https://pypi.org/project/version-helper/
