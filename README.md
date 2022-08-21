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

# Prezzemolo v0.0.2
[![Static Analysis / Main Branch](https://github.com/eprbell/prezzemolo/actions/workflows/static_analysis.yml/badge.svg)](https://github.com/eprbell/prezzemolo/actions/workflows/static_analysis.yml)
[![Documentation Check / Main Branch](https://github.com/eprbell/prezzemolo/actions/workflows/documentation_check.yml/badge.svg)](https://github.com/eprbell/prezzemolo/actions/workflows/documentation_check.yml)
[![Unix Unit Tests / Main Branch](https://github.com/eprbell/prezzemolo/actions/workflows/unix_unit_tests.yml/badge.svg)](https://github.com/eprbell/prezzemolo/actions/workflows/unix_unit_tests.yml)
[![Windows Unit Tests / Main Branch](https://github.com/eprbell/prezzemolo/actions/workflows/windows_unit_tests.yml/badge.svg)](https://github.com/eprbell/prezzemolo/actions/workflows/windows_unit_tests.yml)
[![CodeQL/Main Branch](https://github.com/eprbell/prezzemolo/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/eprbell/prezzemolo/actions/workflows/codeql-analysis.yml)

## Table of Contents
* **[Introduction](https://github.com/eprbell/prezzemolo/tree/main/README.md#introduction)**
* **[License](https://github.com/eprbell/prezzemolo/tree/main/README.md#license)**
* **[Download](https://github.com/eprbell/prezzemolo/tree/main/README.md#download)**
* **[Installation](https://github.com/eprbell/prezzemolo/tree/main/README.md#installation)**
  * [Ubuntu Linux](https://github.com/eprbell/prezzemolo/tree/main/README.md#installation-on-ubuntu-linux)
  * [macOS](https://github.com/eprbell/prezzemolo/tree/main/README.md#installation-on-macos)
  * [Windows 10](https://github.com/eprbell/prezzemolo/tree/main/README.md#installation-on-windows-10)
  * [Other Unix-like Systems](https://github.com/eprbell/prezzemolo/tree/main/README.md#installation-on-other-unix-like-systems)
* **[Reporting Bugs](https://github.com/eprbell/prezzemolo/tree/main/README.md#reporting-bugs)**
* **[Contributing](https://github.com/eprbell/prezzemolo/tree/main/README.md#contributing)**
* **[Developer Documentation](https://github.com/eprbell/prezzemolo/tree/main/README.md#developer-documentation)**
* **[Frequently Asked Questions](https://github.com/eprbell/prezzemolo/tree/main/README.md#frequently-asked-questions)**
* **[Change Log](https://github.com/eprbell/prezzemolo/tree/main/README.md#change-log)**

## Introduction
Prezzemolo is a collection of classic data structure and algorithms that are useful in many different projects. The goal is to provide components that are robust, efficient and small (in decreasing order of importance). Each component has extensive unit testing to reduce the risk of regression. The project will grow organically as new components are needed in various projects, such as RP2 (the privacy-focused, open-source crypto tax calculator), and others.

**IMPORTANT DISCLAIMERS**:
* Prezzemolo offers no guarantee of correctness (read the [license](https://github.com/eprbell/prezzemolo/tree/main/LICENSE)).

## License
Prezzemolo is released under the terms of Apache License Version 2.0. For more information see [LICENSE](https://github.com/eprbell/prezzemolo/tree/main/LICENSE) or <http://www.apache.org/licenses/LICENSE-2.0>.

## Download
The latest version of Prezzemolo can be downloaded at: <https://pypi.org/project/prezzemolo/>

## Installation
Prezzemolo has been tested on Ubuntu Linux, macOS and Windows 10 but it should work on all systems that have Python version 3.7.0 or greater.

### Installation on Ubuntu Linux
Open a terminal window and enter the following commands:
```
sudo apt-get update
sudo apt-get install python3 python3-pip
```

Then install Prezzemolo:
```
pip install prezzemolo
```
### Installation on macOS
First make sure [Homebrew](https://brew.sh) is installed, then open a terminal window and enter the following commands:
```
brew update
brew install python3
```

Then install Prezzemolo:
```
pip install prezzemolo
```
### Installation on Windows 10
First make sure [Python](https://python.org) 3.7 or greater is installed (in the Python installer window be sure to click on "Add Python to PATH"), then open a PowerShell window and enter the following:
```
pip install prezzemolo
```

### Installation on Other Unix-like Systems
* install python 3.7 or greater
* install pip3
* `pip install prezzemolo`

## Reporting Bugs
Read the [Contributing](https://github.com/eprbell/prezzemolo/tree/main/CONTRIBUTING.md#reporting-bugs) document.

## Contributing
Read the [Contributing](https://github.com/eprbell/prezzemolo/tree/main/CONTRIBUTING.md) document.

## Developer Documentation
Read the [developer documentation](https://github.com/eprbell/prezzemolo/tree/main/README.dev.md).

## Frequently Asked Questions
Read the [user FAQ list](https://github.com/eprbell/prezzemolo/tree/main/docs/user_faq.md) and the [developer FAQ list](https://github.com/eprbell/prezzemolo/tree/main/docs/developer_faq.md).

## Change Log
Read the [Change Log](https://github.com/eprbell/prezzemolo/tree/main/CHANGELOG.md) document.
