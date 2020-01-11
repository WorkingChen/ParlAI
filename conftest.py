#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


"""
This is used to configure markers on tests based on filename.

We use this to split up tests into different circleci runs.
"""

import pathlib


# TODO: rename the folders nicer so they make more sense, maybe even have
# a 1:1 correspondance with the circleci name


def pytest_collection_modifyitems(config, items):
    # python 3.4/3.5 compat: rootdir = pathlib.Path(str(config.rootdir))
    rootdir = pathlib.Path(config.rootdir)
    for item in items:
        rel_path = str(pathlib.Path(item.fspath).relative_to(rootdir))
        if "nightly/gpu/" in rel_path:
            item.add_marker("nightly_gpu")
        elif "nightly/cpu/" in rel_path:
            item.add_marker("nightly_cpu")
        elif "datatests/" in rel_path:
            item.add_marker("data")
        elif "tasks/" in rel_path:
            item.add_marker("tasks")
        elif rel_path.startswith("parlai/mturk/core/test"):
            item.add_marker("mturk")
        elif rel_path.startswith("tests/") and "/" not in rel_path[6:]:
            item.add_marker("unit")
        else:
            raise ValueError(f"Couldn't categorize 'rel_path'")
