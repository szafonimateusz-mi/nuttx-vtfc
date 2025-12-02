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

"""NTFC  plugin for pytest."""

from typing import TYPE_CHECKING, List, Tuple

if TYPE_CHECKING:
    import pytest

    from ntfc.pytest.collecteditem import CollectedItem

###############################################################################
# Class: Collected
###############################################################################


class Collected:
    """Collected tests return data."""

    def __init__(
        self,
        items: List["CollectedItem"],
        skipped: List[Tuple["pytest.Item", str]],
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
    def items(self) -> List["CollectedItem"]:
        """Get collected items."""
        return self._items

    @property
    def skipped(self) -> List[Tuple["pytest.Item", str]]:
        """Get skipped items."""
        return self._skipped

    @property
    def modules(self) -> List[str]:
        """Get collected modules."""
        return self._modules
