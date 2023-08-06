#!/bin/false
# -*- coding: utf-8 -*-

""" Functions for locating files and folders on the local filesystem. """

# ------------------------------------------------------------------------------------------------------------------------
# Main imports
# ------------------------------------------------------------------------------------------------------------------------
import os
import pytest
import tempfile
import shutil
from ptutils.globbing import scan_folder, get_subdirs, get_subfiles

FILE_STRUCTURE = {
    "boring_things": {
        "json_thing":      '{ "a": 1, "b": True, "c": 123.45, "d": "hello world" }',
        "text_thing":      'this is file 2',
        "tbd_things": {
        }
    },
    "interesting_things": {
        "scary_thing": "Dracula",
        "silly_thing": "Spongebob",
        "bright_thing": "The sun",
        "heavy_things": {
            "divorce": "nope",
            "lead": "plumbum"
        },
        "auto_things": {
            "mobile": "car",
            "graph": "signature"
        },
        "missing_things": {}
    },
    "apples": {
        "granny-smith": "green",
        "red-delicious": "red"
    },
    "a_file": "some content",
    "another_file": "some other content"
}
PATH_THINGS = []
PATH_BORING_THINGS = ["boring_things"]
PATH_TBD_THINGS = ["boring_things", "tbd_things"]
PATH_INTERESTING_THINGS = ["interesting_things"]
PATH_HEAVY_THINGS = ["interesting_things", "heavy_things"]
PATH_AUTO_THINGS_THINGS = ["interesting_things", "auto_things"]
PATH_MISSING_THINGS = ["interesting_things", "missing_things"]
PATH_APPLES = ["apples"]

THING_SUBDIRS = [["boring_things"], ["interesting_things"], ["apples"]]
THING_SUBFILES = [["a_file"], ["another_file"]]
THING_SUBS = THING_SUBDIRS + THING_SUBFILES

THING_SUBDIRS_REC = [
    PATH_BORING_THINGS,
    PATH_TBD_THINGS,
    PATH_INTERESTING_THINGS,
    PATH_HEAVY_THINGS,
    PATH_AUTO_THINGS_THINGS,
    PATH_MISSING_THINGS,
    PATH_APPLES
]
THING_SUBFILES_REC = [
    ["a_file"],
    ["another_file"],
    PATH_BORING_THINGS + ["json_thing"],
    PATH_BORING_THINGS + ["text_thing"],
    PATH_INTERESTING_THINGS + ["scary_thing"],
    PATH_INTERESTING_THINGS + ["silly_thing"],
    PATH_INTERESTING_THINGS + ["bright_thing"],
    PATH_HEAVY_THINGS + ["divorce"],
    PATH_HEAVY_THINGS + ["lead"],
    PATH_AUTO_THINGS_THINGS + ["mobile"],
    PATH_AUTO_THINGS_THINGS + ["graph"],
    PATH_APPLES + ["granny-smith"],
    PATH_APPLES + ["red-delicious"],
]

THING_KEYED_SUBFILES_REC = [
    PATH_BORING_THINGS + ["json_thing"],
    PATH_BORING_THINGS + ["text_thing"],
    PATH_INTERESTING_THINGS + ["scary_thing"],
    PATH_INTERESTING_THINGS + ["silly_thing"],
    PATH_INTERESTING_THINGS + ["bright_thing"],
]

STARTS_WITH_A_REC = [
    ["a_file"],
    ["another_file"],
    PATH_AUTO_THINGS_THINGS,
    PATH_APPLES
]


def populate(path, content):
    if isinstance(content, dict):
        os.makedirs(path, exist_ok=True)
        for (k, v) in content.items():
            populate(os.path.join(path, k), v)
    elif isinstance(content, str):
        with open(path, "w") as filp:
            filp.write(content)
    else:
        raise Exception("BUG: content is not a string and is not a dict.")


@pytest.fixture(autouse=True)
def sample_file_structure():
    dir = tempfile.TemporaryDirectory()
    populate(dir.name, FILE_STRUCTURE)
    yield dir.name
    shutil.rmtree(dir.name)


QUERIES = [
    # (path, pattern, recursive, filter_func, expected_relpaths)
    (PATH_THINGS, None, False, None,           THING_SUBS),
    (PATH_THINGS, None, False, os.path.isfile, THING_SUBFILES),
    (PATH_THINGS, None, False, os.path.isdir,  THING_SUBDIRS),
    (PATH_THINGS, None, True,  os.path.isfile, THING_SUBFILES_REC),
    (PATH_THINGS, None, True, os.path.isdir,  THING_SUBDIRS_REC),
    (PATH_THINGS, r'^.*_thing$', True, None,  THING_KEYED_SUBFILES_REC),
    (PATH_THINGS, r'^a.*$', True, None,  STARTS_WITH_A_REC),
]


@pytest.mark.parametrize(
    ["path", "pattern", "recursive", "filterfunc", "expected"],
    QUERIES,
    ids = [f"QUERIES[{i}]" for i in range(len(QUERIES))]
)
def test_scan_folder(sample_file_structure, path, pattern, recursive, filterfunc, expected):
    folder = os.path.join(sample_file_structure, *path)
    items = list(scan_folder(
        folder     = folder,
        pattern    = pattern,
        recursive  = recursive,
        filterfunc = filterfunc
    ))
    items_rel    = set([os.path.relpath(item, sample_file_structure) for item in items])
    expected_rel = set([os.path.join(*parts) for parts in expected])
    assert bool(items_rel)
    assert bool(expected_rel)
    assert items_rel == expected_rel


@pytest.mark.parametrize(
    ["path", "pattern", "recursive", "filterfunc", "expected"],
    QUERIES,
    ids = [f"QUERIES[{i}]" for i in range(len(QUERIES))]
)
def test_get_subdirs(sample_file_structure, path, pattern, recursive, filterfunc, expected):
    if filterfunc is os.path.isdir:
        folder = os.path.join(sample_file_structure, *path)
        items = list(get_subdirs(
            folder     = folder,
            pattern    = pattern,
            recursive  = recursive
        ))
        items_rel    = set([os.path.relpath(item, sample_file_structure) for item in items])
        expected_rel = set([os.path.join(*parts) for parts in expected])
        assert bool(items_rel)
        assert bool(expected_rel)
        assert items_rel == expected_rel


@pytest.mark.parametrize(
    ["path", "pattern", "recursive", "filterfunc", "expected"],
    QUERIES,
    ids = [f"QUERIES[{i}]" for i in range(len(QUERIES))]
)
def test_get_subfiles(sample_file_structure, path, pattern, recursive, filterfunc, expected):
    if filterfunc is os.path.isfile:
        folder = os.path.join(sample_file_structure, *path)
        items = list(get_subfiles(
            folder     = folder,
            pattern    = pattern,
            recursive  = recursive
        ))
        items_rel    = set([os.path.relpath(item, sample_file_structure) for item in items])
        expected_rel = set([os.path.join(*parts) for parts in expected])
        assert bool(items_rel)
        assert bool(expected_rel)
        assert items_rel == expected_rel
