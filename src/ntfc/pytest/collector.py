############################################################################
# SPDX-License-Identifier: Apache-2.0
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.  The
# ASF licenses this file to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance with the
# License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations
# under the License.
#
############################################################################

"""NTFC collector plugin for pytest."""

import os
from typing import Any, List, Tuple

import pytest

from ntfc.pytest.collecteditem import CollectedItem

###############################################################################
# Class: CollectorPlugin
###############################################################################


class CollectorPlugin:
    """Custom Pytest collector plugin."""

    def __init__(self) -> None:
        """Initialize custom pytest collector plugin."""
        self.collected_items: List[Tuple[Any, Any]] = []
        self.parsed_items: List[CollectedItem] = []

    @property
    def parsed(self) -> List[CollectedItem]:
        """Get collected items in parsed format."""
        return self.parsed_items

    def pytest_runtestloop(self, session: pytest.Session) -> bool:
        """Prevent tests from running.

        Returning True stops test execution.
        """
        return True

    def pytest_collection_finish(self, session: pytest.Session) -> None:
        """Pytest collection finish callback."""
        self.collected_items.extend(session.items)

        # extract useful data from items
        for item in session.items:
            path, lineno, name = item.location
            abs_path = os.path.abspath(path)
            directory = os.path.dirname(abs_path)
            module = abs_path.replace(pytest.testpath, "")
            root = module.replace(pytest.testpath, "")

            ci = CollectedItem(
                directory,
                module,
                name,
                abs_path,
                lineno,
                item.nodeid,
                pytest.ntfcyaml["module"],
                root,
            )
            self.parsed_items.append(ci)
