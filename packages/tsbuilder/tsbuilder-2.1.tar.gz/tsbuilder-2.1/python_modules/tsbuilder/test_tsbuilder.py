# This file is part of the Test-Comp test format,
# an exchange format for test suites:
# https://gitlab.com/sosy-lab/software/test-format
#
# Copyright (C) 2018  Dirk Beyer
# SPDX-FileCopyrightText: 2018-2019 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

"""Tests for tsbuilder module."""

import datetime
from urllib import request
from lxml import etree
import tsbuilder as tf
from tsbuilder import architecture
from tsbuilder import specs


class DTDResolver(etree.Resolver):
    def resolve(self, url, d_id, context):
        if url.startswith("http"):
            with request.urlopen(url) as inp:
                dtd_content = inp.read()
            return self.resolve_string(dtd_content, context)
        return super().resolve(url, d_id, context)


PARSER = etree.XMLParser(dtd_validation=True)
"""XML parser used in unit tests."""
PARSER.resolvers.add(DTDResolver())
TEST_FILE = "test/test.c"
"""Dummy test file used in unit tests."""
DATE = datetime.datetime.min
"""Dummy date used in unit tests."""


def test_metadatabuilder_none_arguments():
    """Test that MetadataBuilder does not allow None for its required arguments."""
    valid_args = (
        "C",
        "Human v1.5",
        specs.STATEMENT_COVERAGE,
        TEST_FILE,
        "main",
        architecture.LINUX32,
        DATE,
    )
    none_args = [None] * len(valid_args)
    args = list(zip(valid_args, none_args))
    # check for each argument to builder, that a TypeError is thrown if it is None
    for i in range(0, len(valid_args)):
        curr_args = [x[1] if i == idx else x[0] for idx, x in enumerate(args)]
        assert len(valid_args) == len(curr_args)
        try:
            tf.MetadataBuilder(*curr_args)
        except TypeError:
            pass  # expected, continue
        else:
            assert False, "Expected TypeError because of None argument"


def test_metadatabuilder_empty_arguments():
    """Test that MetadataBuilder does not allow an empty string for its required arguments."""
    valid_args = (
        "C",
        "Human v1.5",
        specs.STATEMENT_COVERAGE,
        TEST_FILE,
        "main",
        architecture.LINUX32,
        DATE,
    )
    empty_args = [""] * len(valid_args)
    args = list(zip(valid_args, empty_args))
    # check for each argument to builder, that a TypeError is thrown if it is None
    for i in range(0, len(valid_args)):
        curr_args = [x[1] if i == idx else x[0] for idx, x in enumerate(args)]
        assert len(valid_args) == len(curr_args)
        try:
            tf.MetadataBuilder(
                *[x[1] if i == idx else x[0] for idx, x in enumerate(args)]
            )
        except ValueError:
            pass  # expected, continue
        else:
            assert False, "Expected ValueError because of empty string"


def test_metadata_builder():
    """Test that a metadata builder with valid args is built successfully."""
    builder = tf.MetadataBuilder(
        "C",
        "Human v1.5",
        specs.STATEMENT_COVERAGE,
        TEST_FILE,
        "main",
        architecture.LINUX32,
        creation_time=DATE,
    )

    assert _is_build_valid(builder)


def test_metadata_builder_inputtestsuite():
    """Test that a metadata builder with valid args and input test-suite is built successfully."""
    builder = tf.MetadataBuilder(
        "C",
        "Human v1.5",
        specs.STATEMENT_COVERAGE,
        TEST_FILE,
        "main",
        architecture.LINUX32,
        creation_time=DATE,
        inputsuitefile="test/suite.zip",
    )

    assert _is_build_valid(builder)


def test_testcasebuilder_empty():
    """Test that building from TestcaseBuilder without a testcase raises an error."""
    builder = tf.TestcaseBuilder()

    try:
        builder.build()
    except AttributeError:
        pass
    else:
        assert False, "Expected AttributeError due to missing test case"


def test_testcasebuilder_input():
    """Test that test input values are accepted in different formats."""

    assert all(
        _check_testcasebuilder_input(inp)
        for inp in ("5", 5, "Multiline\nString", b"ByteString", "\\x00\\x50\\x10\\x40")
    )


def _check_testcasebuilder_input(inp):
    builder = tf.TestcaseBuilder()
    builder.test_case_start().input_val(inp)

    return _is_build_valid(builder)


def test_testcasebuilder_input_attributes():
    """Test that the attributes of test input values can be set to different values."""
    builder = tf.TestcaseBuilder()
    builder.test_case_start().input_val(
        "17", variable="xy", value_type="char *"
    ).input_val("15", variable="y").input_val("1395", value_type="unsigned char")

    assert _is_build_valid(builder)


def test_testcasebuilder_coverserror():
    """Test that a test case with coversError=true is built successfully."""
    builder = tf.TestcaseBuilder()
    builder.test_case_start(covers_error=True)

    assert _is_build_valid(builder)


def _is_build_valid(builder):
    created_xml = builder.build()

    etree.fromstring(created_xml, PARSER)
    return True
