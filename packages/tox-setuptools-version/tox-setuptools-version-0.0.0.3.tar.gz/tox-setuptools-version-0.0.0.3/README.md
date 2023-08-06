[![Build Status](https://dev.azure.com/LvffY/LvffY/_apis/build/status/LvffY.tox-setuptools-version?branchName=master)](https://dev.azure.com/LvffY/LvffY/_build/latest?definitionId=1&branchName=master)
![](https://img.shields.io/pypi/v/tox-setuptools-version.svg)
![](https://img.shields.io/pypi/pyversions/tox-setuptools-version.svg)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=LvffY_tox-setuptools-version&metric=coverage)](https://sonarcloud.io/dashboard?id=LvffY_tox-setuptools-version)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=LvffY_tox-setuptools-version&metric=bugs)](https://sonarcloud.io/dashboard?id=LvffY_tox-setuptools-version)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=LvffY_tox-setuptools-version&metric=code_smells)](https://sonarcloud.io/dashboard?id=LvffY_tox-setuptools-version)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=LvffY_tox-setuptools-version&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=LvffY_tox-setuptools-version)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=LvffY_tox-setuptools-version&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=LvffY_tox-setuptools-version)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=LvffY_tox-setuptools-version&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=LvffY_tox-setuptools-version)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=LvffY_tox-setuptools-version&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=LvffY_tox-setuptools-version)


Overview
--------

This is a tox plugin that preinstalls a specific version of setuptools in each tox
environment.

```bash
pip install tox-setuptools-version
```

This works around the default behavior of tox/virtualenv that always installs
the latest version setuptools. It is an improvement over the `VIRTUALENV_NO_DOWNLOAD=1`
option that does not install the latest version, but could result in usage of
an outdated version of setuptools.

*Note*: This relies on an [unstable tox plugin interface](
https://tox.readthedocs.io/en/latest/plugins.html#tox.hookspecs.tox_testenv_create).
You may experience breakage with new tox versions. If you do, please feel
free to [report the issue](https://github.com/LvffY/tox-setuptools-version/issues/new)
on Github.

This repository is based on a fork from the plugin [tox-pip-version](https://github.com/pglass/tox-pip-version), you should probably go to see his job too.

### Usage

Install the package and include `setuptools_version` in your tox.ini

```tox
[testenv]
setuptools_version = setuptools_version<58
```

Or, set the `TOX_SETUPTOOLS_VERSION` environment variable,

```bash
export TOX_SETUPTOOLS_VERSION=57.2.4
tox
```

The plugin will install that version of setuptools into the tox-created virtualenv,
just after tox creates the virtualenv, but before dependencies are installed.

The `setuptools_version` within tox.ini, if present, is always used over the
environment variable.

If neither `setuptools_version` or `TOX_SETUPTOLLS_VERSION` is present, the plugin does
nothing.

### Version Sets

Version sets/ranges are supported, enabling installation of a version of pip
matching a set of specifiers. There are two basic formats: a plain version
number, or the package name with optional [PEP440-compatible](
https://www.python.org/dev/peps/pep-0440/#version-specifiers) version
specifiers.

| tox.ini                      | effective pip command        |
| ---------------------------- | ---------------------------- |
| `setuptools_version = 58.0`         | `pip install -U setuptools==19.0`   |
| `setuptools_version = setuptools==58.0`    | `pip install -U setuptools==58.0`   |
| `setuptools_version = setuptools>=58.0`    | `pip install -U setuptools>=58.0`   |
| `setuptools_version = setuptools!=58.0,>57`  | `pip install -U setuptools!=58.0,>57` |
| `setuptools_version = setuptools`          | `pip install -U setuptools`         |
| `setuptools_version = setuptools@git+https://github.com/pypa/setuptools@0168ac6` | `setuptools@git+https://github.com/pypa/setuptools@0168ac6` |
