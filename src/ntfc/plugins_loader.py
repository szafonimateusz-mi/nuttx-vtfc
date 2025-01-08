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

"""Plugins loader."""

from importlib.metadata import entry_points
from typing import TYPE_CHECKING

import ntfc.ext_commands
from ntfc.logger import logger

if TYPE_CHECKING:
    import click

commands_list: list["click.Command"] = []

# default commands
commands_list.extend(ntfc.ext_commands.commands_list)

# load external plugins
eps = entry_points(group="ntfc.extensions")
for entry in eps:  # pragma: no cover
    logger.info("loading %s %s ...", entry.name, entry.value)
    plugin = entry.load()
    if entry.name == "commands":
        commands_list.extend(plugin.commands_list)
    else:
        raise AssertionError("Unsupported entry name")
