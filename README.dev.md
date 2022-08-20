<!--- Copyright 2022 eprbell --->

<!--- Licensed under the Apache License, Version 2.0 (the "License"); --->
<!--- you may not use this file except in compliance with the License. --->
<!--- You may obtain a copy of the License at --->

<!---     http://www.apache.org/licenses/LICENSE-2.0 --->

<!--- Unless required by applicable law or agreed to in writing, software --->
<!--- distributed under the License is distributed on an "AS IS" BASIS, --->
<!--- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. --->
<!--- See the License for the specific language governing permissions and --->
<!--- limitations under the License. --->

# Prezzemolo v0.0.1 Developer Guide
[![Static Analysis / Main Branch](https://github.com/eprbell/prezzemolo/actions/workflows/static_analysis.yml/badge.svg)](https://github.com/eprbell/prezzemolo/actions/workflows/static_analysis.yml)
[![Documentation Check / Main Branch](https://github.com/eprbell/prezzemolo/actions/workflows/documentation_check.yml/badge.svg)](https://github.com/eprbell/prezzemolo/actions/workflows/documentation_check.yml)
[![Unix Unit Tests / Main Branch](https://github.com/eprbell/prezzemolo/actions/workflows/unix_unit_tests.yml/badge.svg)](https://github.com/eprbell/prezzemolo/actions/workflows/unix_unit_tests.yml)
[![Windows Unit Tests / Main Branch](https://github.com/eprbell/prezzemolo/actions/workflows/windows_unit_tests.yml/badge.svg)](https://github.com/eprbell/prezzemolo/actions/workflows/windows_unit_tests.yml)
[![CodeQL/Main Branch](https://github.com/eprbell/prezzemolo/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/eprbell/prezzemolo/actions/workflows/codeql-analysis.yml)

## Table of Contents
* **[Introduction](#introduction)**
* **[License](#license)**
* **[Download](#download)**
* **[Setup](#setup)**
  * [Ubuntu Linux](#setup-on-ubuntu-linux)
  * [macOS](#setup-on-macos)
  * [Windows 10](#setup-on-windows-10)
  * [Other Unix-like Systems](#setup-on-other-unix-like-systems)
* **[Source Code](#source-code)**
* **[Development](#development)**
  * [Design Guidelines](#design-guidelines)
  * [Development Workflow](#development-workflow)
  * [Unit Tests](#unit-tests)
* **[Creating a Release](#creating-a-release)**
* **[Localization](#localization)**
* **[Frequently Asked Developer Questions](#frequently-asked-developer-questions)**

## Introduction
This document describes [Prezzemolo](https://github.com/eprbell/prezzemolo) setup instructions, development workflow, design principles and source tree structure.

## License
Prezzemolo is released under the terms of Apache License Version 2.0. For more information see [LICENSE](LICENSE) or <http://www.apache.org/licenses/LICENSE-2.0>.

## Download
The latest Prezzemolo source can be downloaded at: <https://github.com/eprbell/prezzemolo>

## Setup
Prezzemolo has been tested on Ubuntu Linux, macOS and Windows 10 but it should work on all systems that have Python version 3.7.0 or greater. Virtualenv is recommended for Prezzemolo development.

### Setup on Ubuntu Linux
First make sure Python, pip and virtualenv are installed. If not, open a terminal window and enter the following commands:
```
sudo apt-get update
sudo apt-get install python3 python3-pip virtualenv
```

Then install Prezzemolo Python package requirements:
```
cd <prezzemolo_directory>
virtualenv -p python3 .venv
. .venv/bin/activate
.venv/bin/pip3 install -e '.[dev]'
```
### Setup on macOS
First make sure [Homebrew](https://brew.sh) is installed, then open a terminal window and enter the following commands:
```
brew update
brew install python3 virtualenv
```

Then install Prezzemolo Python package requirements:
```
cd <prezzemolo_directory>
virtualenv -p python3 .venv
. .venv/bin/activate
.venv/bin/pip3 install -e '.[dev]'
```
### Setup on Windows 10
First make sure [Python](https://python.org) 3.7 or greater is installed (in the Python installer window be sure to click on "Add Python to PATH"), then open a PowerShell window and enter the following commands:
```
python -m pip install virtualenv
```

Then install Prezzemolo Python package requirements:
```
cd <prezzemolo_directory>
virtualenv -p python .venv
.venv\Scripts\activate.ps1
python -m pip install -e ".[dev]"
```
### Setup on Other Unix-like Systems
* install python 3.7 or greater
* install pip3
* install virtualenv
* cd _<prezzemolo_directory>_
* `virtualenv -p python3 .venv`
* `.venv/bin/pip3 install -e '.[dev]'`

## Source Code
The Prezzemolo source tree is organized as follows:
* `.bumpversion.cfg`: bumpversion configuration;
* `CHANGELOG.md`: change log document;
* `CONTRIBUTING.md`: contribution guidelines;
* `docs/`: additional documentation, referenced from the README files;
* `.editorconfig`;
* `.gitattributes`;
* `.github/workflows/`: configuration of Github continuous integration;
* `.gitignore`;
* `.isort.cfg`: isort configuration;
* `LICENSE`: license information;
* `Makefile`: alternative old-school build flow;
* `MANIFEST.in`: source distribution configuration;
* `mypy.ini`: mypy configuration;
* `.pre-commit-config.yaml`: pre-commit configuration;
* `.pylintrc`: pylint configuration;
* `pyproject.toml`: packaging configuration;
* `README.dev.md`: developer documentation;
* `README.md`: user documentation;
* `setup.cfg`: static packaging configuration file;
* `setup.py`: dynamic packaging configuration file;
* `src/prezzemolo`: Prezzemolo code, including classes for transactions, gains, tax engine, balances, logger, ODS parser, etc.;
* `tests/`: unit tests.

## Development
Read the [Contributing](CONTRIBUTING.md) document on pull requests guidelines.

### Design Guidelines
Prezzemolo code adheres to these principles:
* all identifiers have [descriptive names](https://realpython.com/python-pep8/#how-to-choose-names);
* immutability:
  * global variables have upper case names, are initialized where declared and are never modified afterwards;
  * generally data structures are read-only (the only exceptions are for data structures that would incur a major complexity increase without write permission: e.g. AVL tree node):
    * class fields are private (prepended with double-underscore). Fields that need public access have a read-only property. Write-properties are not used;
    * @dataclass classes have `frozen=True`;
* runtime checks: parameters of public functions are type-checked at runtime;
* type hints: all variables and functions have Python type hints (with the exception of local variables, for which type hints are optional);
* no id-based hashing: classes that are added to dictionaries and sets redefine `__eq__()`, `__neq__()` and `__hash__()`;
* f-strings only: every time string interpolation is needed, f-strings are used;
* no raw strings (unless they occur only once): use global constants instead;
* no unnamed tuples: dataclasses or named tuples are used instead;
* one class per file (with exceptions for trivial classes);
* files containing a class must have the same name as the class (but lowercase with underscores): e.g. class AbstractEntry lives in file abstract_entry.py;
* abstract class names start with `Abstract`;
* no imports with `*`.

### Development Workflow
Prezzemolo uses pre-commit hooks for quick validation at commit time and continuous integration via Github actions for deeper testing. Pre-commit hooks invoke: flake8, black, isort, pyupgrade and more. Github actions invoke: mypy, pylint, bandit, unit tests (on Linux, Mac and Windows), markdown link check and more.

While every commit and push is automatically tested as described, sometimes it's useful to run some of the above commands locally without waiting for continuous integration. Here's how to run the most common ones:
* run unit tests: `pytest --tb=native --verbose`
* type check: `mypy src tests`
* lint: `pylint -r y src tests/*.py`
* security check: `bandit -r src`
* reformat code: `black src tests`
* sort imports: `isort .`
* run pre-commit tests without committing: `pre-commit run --all-files`

### Unit Tests
Prezzemolo has unit test coverage to reduce the risk of regression. Unit tests are in the [tests](tests) directory. Please add unit tests for any new code.

## Creating a Release
This section is for project maintainers.

To create a new release:
* add a section named as the new version in CHANGELOG.md
* use the output of `git log` to collect significant changes since last version and add them to CHANGELOG.md as a list of brief bullet points
* `git add CHANGELOG.md`
* `git commit -m "Updated with latest changes" CHANGELOG.md`
* `bumpversion patch` (or `bumpversion minor` or `bumpversion major`)
* `git push`
* wait for all tests to pass successfully on Github
* add a tag in Github (named the same as the version but with a `v` in front, e.g. `v1.0.4`):  click on "Releases" and then "Draft a new release"

To create a Pypi distribution:
* `make distribution`
* `make upload_distribution`

## Frequently Asked Developer Questions
Read the [frequently asked developer questions](docs/developer_faq.md).
