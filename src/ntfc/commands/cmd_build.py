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

"""Module containing NTFC collect command."""

import click

from ntfc.cli.clitypes import cli_confpath_option
from ntfc.cli.environment import Environment, pass_environment

###############################################################################
# Command: cmd_build
###############################################################################


@click.command(name="build")
@cli_confpath_option
@click.option(
    "--noflash",
    default=False,
    is_flag=True,
)
@pass_environment
def cmd_build(ctx: Environment, confpath: str, noflash: bool) -> bool:
    """Build only command."""
    ctx.runbuild = True
    ctx.confpath = confpath
    ctx.noflash = noflash

    return True
