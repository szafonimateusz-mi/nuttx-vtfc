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

###############################################################################
# Class: CollectedItem
###############################################################################


class CollectedItem:
    """Collected test item."""

    def __init__(
        self,
        directory: str,
        module: str,
        name: str,
        path: str,
        line: int,
        nodeid: str,
        modname: str,
        root: str,
    ) -> None:
        """Initialzie collection item."""
        self._directory = directory
        self._module = module
        self._name = name
        self._path = path
        self._line = line
        self._nodeid = nodeid
        self._module2 = modname + "_".join(
            part.capitalize() for part in root.split("/")[:-1]
        )

    def __str__(self) -> str:
        """Get collected item string representation."""
        _str = "CollectedItem: " + self.name
        return _str

    @property
    def module2(self) -> str:
        """Get collected module name (short version)."""
        return self._module2

    @property
    def directory(self) -> str:
        """Get collected item directory."""
        return self._directory

    @property
    def module(self) -> str:
        """Get collected item module."""
        return self._module

    @property
    def name(self) -> str:
        """Get collected item name."""
        return self._name

    @property
    def path(self) -> str:
        """Get collected item file."""
        return self._path

    @property
    def line(self) -> int:
        """Get collected item line."""
        return self._line

    @property
    def nodeid(self) -> str:
        """Get collected item node ID."""
        return self._nodeid


###############################################################################
# Class: Collected
###############################################################################


class Collected:
    """Collected tests return data."""

    def __init__(
        self,
        items: List[CollectedItem],
        skipped: List[Tuple[pytest.Item, str]],
    ):
        """Initialize test collected data."""
        self._items = items
        self._skipped = skipped
        self._modules = self._get_modules()

    def _get_modules(self) -> List[str]:
        """Get collected modules."""
        mod = set()
        for i in self._items:
            mod.add(i.module2)
        return list(mod)

    @property
    def items(self) -> List[CollectedItem]:
        """Get collected items."""
        return self._items

    @property
    def skipped(self) -> List[Tuple[pytest.Item, str]]:
        """Get skipped items."""
        return self._skipped

    @property
    def modules(self) -> List[str]:
        """Get collected modules."""
        return self._modules


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
