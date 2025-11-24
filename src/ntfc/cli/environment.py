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

"""Module containing the Click environment."""

from dataclasses import dataclass

import click

###############################################################################
# Class: DEnvironmentData
###############################################################################


@dataclass
class DEnvironmentData:
    """Environment data."""

    helpnow: bool = False
    debug: bool = False
    verbose: bool = False
    exitonfail: bool = False
    runcollect: bool = False
    buildonly: bool = False
    noflash: bool = False
    runtest: bool = False
    runprint: bool = False
    nologs: bool = False
    testpath: str = None
    confpath: str = None
    ignorefile: str = None
    result: dir = None
    collect: str = None
    confjson: str = None


###############################################################################
# Class: Environment
###############################################################################


class Environment(DEnvironmentData):
    """A class with application environment."""

    def __init__(self) -> None:
        """Initialize environment."""
        super().__init__()


###############################################################################
# Decorator: pass_environment
###############################################################################


# custom environment decorator
pass_environment = click.make_pass_decorator(Environment, ensure=True)
