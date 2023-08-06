# This file is part of the Test-Comp test format,
# an exchange format for test suites:
# https://gitlab.com/sosy-lab/software/test-format
#
# Copyright (C) 2018  Dirk Beyer
# SPDX-FileCopyrightText: 2018-2019 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

"""Module for easy creation of test-format XML files.

The Builder class is the only relevant component of this module.

Sub-modules are available and provide constants for common metadata:
    * tsbuilder.architecture
    * tsbuilder.specs
"""

import hashlib
import datetime
from lxml import etree as ET

__VERSION__ = "2.1"

METADATA_DTD = (
    '<!DOCTYPE test-metadata PUBLIC "+//IDN sosy-lab.org//DTD'
    + ' test-format test-metadata 1.1//EN"'
    + ' "https://sosy-lab.org/test-format/test-metadata-1.1.dtd">'
)
TESTCASE_DTD = (
    '<!DOCTYPE testcase PUBLIC "+//IDN sosy-lab.org//DTD'
    + ' test-format testcase 1.1//EN"'
    + ' "https://sosy-lab.org/test-format/testcase-1.1.dtd">'
)


class MetadataBuilder:
    """Builder for test-format metadata XML files.

    Provides methods to build an XML that describes the metadata of a test suite in the
    test format.
    """

    def __init__(
        self,
        sourcecode_language,
        producer,
        specification,
        programfile,
        entryfunction,
        architecture,
        creation_time,
        inputsuitefile=None,
    ):
        """Create a new Builder object with the given metadata.

        Requires all metadata that is mandatory for the test format.

        :param str sourcecode_language: Source-code language of the tested program
        :param str producer: Name of the producer of the test suite.
            May contain version information to improve reproducability and documentation.
        :param str specification: The specification the test suite covers.
            Should be the exact specification string, not the path to a file containing it.
        :param str programfile: Name of the tested program. May contain path information.
        :param str entryfunction: Name of the function through which the tested program was entered.
            In most cases, this will be `main`, but other functions are possible.
        :param str architecture: System architecture for which the test suite was created.
            Usual values are `32bit` or `64bit`.
        :param datetime.datetime creation_time: Creation time and date of the test suite
        :param Optional[str] inputsuitefile: Test suite file from which the test suite
            of this metadata object was derived (e.g., through test-suite reduction)
        :raises TypeError: If any required argument is None
        :raises ValueError: If any required argument is an empty string
        """
        self._sourcecode_language = _check_not_none(sourcecode_language)
        self._producer = _check_not_none(producer)
        self._specification = _check_not_none(specification)
        self._programfile = _check_not_none(programfile)
        self._entryfunction = _check_not_none(entryfunction)
        self._architecture = _check_not_none(architecture)
        self._creation_time = _check_not_none(creation_time)
        self._inputsuitefile = inputsuitefile

    @property
    def _programhash(self):
        return self._create_hash(self._programfile)

    @property
    def _inputtestsuitehash(self):
        if not self._inputsuitefile:
            return None
        return self._create_hash(self._inputsuitefile)

    @staticmethod
    def _create_hash(file_path):
        hash_creator = hashlib.sha1()
        with open(file_path, "rb") as inp:
            hash_creator.update(inp.read())
        return hash_creator.hexdigest()

    def build(self):
        """Build the final XML based on the information present in the builder.

        Multiple calls to this method on the same object are possible.

        :return: Byte-string representation of the final XML.
        """
        metadata = ET.Element("test-metadata")
        self._add_metadata(metadata)
        return ET.tostring(
            metadata,
            encoding="UTF-8",
            xml_declaration=True,
            pretty_print=True,
            doctype=METADATA_DTD,
        )

    def _add_metadata(self, parent):
        _create_tag(parent, "sourcecodelang", self._sourcecode_language)
        _create_tag(parent, "producer", self._producer)
        _create_tag(parent, "specification", self._specification)
        _create_tag(parent, "programfile", self._programfile)
        _create_tag(parent, "programhash", self._programhash)
        _create_tag(parent, "entryfunction", self._entryfunction)
        _create_tag(parent, "architecture", self._architecture)
        if self._inputsuitefile:
            _create_tag(parent, "inputtestsuitefile", self._inputsuitefile)
            _create_tag(parent, "inputtestsuitehash", self._inputtestsuitehash)
        _create_tag(parent, "creationtime", self._creation_time)


class TestcaseBuilder:
    """Builder for test-format test-case XML files.

    Provides methods to build an XML that describes a test case in the test format.
    """

    def __init__(self):
        self._test_cases = []
        self._current_test_case = None

    def test_case_start(self, covers_error=False):
        """Create a new test case in the test suite under construction.

        Test inputs can be added with method input_val.
        For each created test case, its end must be signified
        by invoking method build_test_case.

        :param bool covers_error: Whether the test case covers a looked-for error.
            Only necessary when specifications for falsification are used.
            By default always false.
        :return: Current builder object for method chaining.
        :raises AttributeError: If another test case was started but not ended yet
            (see build_test_case).
        """
        if self._current_test_case is not None:
            raise AttributeError("Other test case still pending")
        self._current_test_case = {"coversError": covers_error, "inputs": []}
        return self

    def build(self):
        """Mark the current test case as finished and return the XML representation.

        :return: XLM for test case in bytestring representation.
        :raises AttributeError: If no test case was started (see test_case_start).
        """
        if self._current_test_case is None:
            raise AttributeError("No test case started")

        tc_attribs = {}
        if self._current_test_case["coversError"]:
            tc_attribs["coversError"] = "true"
        testcase = ET.Element("testcase", tc_attribs)
        self._add_testcase(testcase, self._current_test_case)
        self._current_test_case = None
        return ET.tostring(
            testcase,
            encoding="UTF-8",
            xml_declaration=True,
            pretty_print=True,
            doctype=TESTCASE_DTD,
        )

    def input_val(self, value, variable=None, value_type=None):
        """Add an input value to the current test case.

        :param value: Input value
        :param variable: Input variable the input value is assigned to.
            This is metadata and currently not required,
            as test-input order is based on their sequence within the test case.
        :param value_type: The type of the input value. This is metadata and currently not required.
        :return: Current builder object for method chaining.
        :raises AttributeError: If no test case was started (see test_case_start).
        """
        if self._current_test_case is None:
            raise AttributeError("No test case started")
        new_input = {"value": value, "variable": variable, "type": value_type}
        self._current_test_case["inputs"].append(new_input)
        return self

    @staticmethod
    def _add_testcase(parent, test_case):
        for inp in test_case["inputs"]:
            inp_attribs = {}
            if inp["variable"]:
                inp_attribs["variable"] = inp["variable"]
            if inp["type"]:
                inp_attribs["type"] = inp["type"]
            _create_tag(parent, "input", inp["value"], inp_attribs)


def _create_tag(parent, name, value, attributes=None):
    if attributes is None:
        attributes = {}
    tag = ET.SubElement(parent, name, attributes)
    value = str(value)
    tag.text = value
    return tag


def _check_not_none(value):
    if value is None:
        raise TypeError("Value none")
    if value == "":
        raise ValueError("Value is empty string")
    return value
