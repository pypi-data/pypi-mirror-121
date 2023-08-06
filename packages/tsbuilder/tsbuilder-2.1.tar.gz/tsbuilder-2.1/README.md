<!--
This file is part of the Test-Comp test format,
an exchange format for test suites:
https://gitlab.com/sosy-lab/software/test-format

SPDX-FileCopyrightText: 2018-2020 Dirk Beyer <https://www.sosy-lab.org>

SPDX-License-Identifier: Apache-2.0
-->

# Test-format

[![Apache 2.0 License](https://img.shields.io/badge/license-Apache--2-brightgreen.svg?style=flat)](https://www.apache.org/licenses/LICENSE-2.0)

This repository contains information about the exchange format
for test suites, as used in the Test-COMP.
It also contains some example-converters from proprietary formats
to the exchange format.

## Exchange format
The goal of the exchange format is to facilitate
easy information exchange between different
automatic test-case generation tools
and towards test-case executors.
The format should allow users to specify test cases
in a both human- and machine-readable format that can be easily reused.

[Read more](doc/Format.md)

## Tool Requirements
For the provided tools, we assume that python 3.5 or later is used
and lxml >= 4.0.0 is installed.

For development, we use `black`, `pylint` and `pytest`.

## Test-convert: Exchange Format ➡ C Unit Tests 

The tool TestCov for test-suite execution has moved to [its own repository](https://gitlab.com/sosy-lab/software/test-suite-validator/)


## Proprietary Formats ➡ Exchange Format

We provide converters for the following tools' test case output formats:

* [AFL](http://lcamtuf.coredump.cx/afl/)
* [CPATiger](https://forsyte.at/software/cpatiger/)
* [Crest](https://crest.github.io)
* [FShell](https://github.com/tautschnig/fshell)
* [KLEE](https://klee.github.io)

The corresponding adaptors can be found in
[python_modules/adaptors](./python_modules/adaptors).
They are designed so that each individual adaptor file
(e.g., `afl.py`), can be used without the other adaptor files.
Each adaptor file usually depends on [`tsbuilder`](python_modules/tsbuilder), `utils.py` and `testcase_converter.py`.

## Support

If you find something not working or know of some improvements,
we're always happy about new issues or pull requests!

Most files in this project are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0)
and have copyright by [Dirk Beyer](https://www.sosy-lab.org/people/beyer/).
