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

"""Module containing the CLI logic for NTFC."""

import sys

import click

from ntfc.builder import NuttXBuilder
from ntfc.cli.environment import Environment, pass_environment
from ntfc.envconfig import EnvConfig
from ntfc.logger import logger
from ntfc.plugins_loader import commands_list
from ntfc.pytest.mypytest import MyPytest

###############################################################################
# Function: main
###############################################################################


@click.group()
@click.option(
    "--debug/--no-debug",
    default=False,
    is_flag=True,
)
@click.option(
    "--verbose/--no-verbose",
    default=False,
    is_flag=True,
)
@pass_environment
def main(ctx: Environment, debug: bool, verbose: bool) -> bool:
    """VFTC - NuttX Testing Framework for Community."""
    ctx.debug = debug
    ctx.verbose = verbose

    if debug:  # pragma: no cover
        logger.setLevel("DEBUG")
    else:
        logger.setLevel("INFO")

    # handle work after all commands are parsed
    click.get_current_context().call_on_close(cli_on_close)

    # check if --help was called
    if "--help" in sys.argv[1:]:  # pragma: no cover
        ctx.helpnow = True

    return True


def collect_print_skipped(items):
    """Print skipped tests and reason."""
    if items:
        print("Skipped tests:")
    for item in items:
        print(f"{item[0].location[0]}:{item[0].location[2]}: \n => {item[1]}")


def collect_run(pt, ctx):
    """Collect tests."""
    col = pt.collect(ctx.testpath)

    print("\nCollect summary:")
    print(f"  collected: {len(col.items)} skipped: {len(col.skipped)}")

    if ctx.collect == "silent":
        return

    if ctx.collect == "collected" or ctx.collect == "all":
        # print parsed test cases
        for item in col.items:
            print(item)

    if ctx.collect == "skipped" or ctx.collect == "all":
        # print skipped test cases
        collect_print_skipped(col.skipped)


def test_run(pt, ctx):
    """Run tests."""
    pt.runner(ctx.testpath, ctx.result, ctx.nologs)


@pass_environment
def cli_on_close(ctx: Environment) -> bool:
    """Handle all work on Click close."""
    if ctx.helpnow:  # pragma: no cover
        # do nothing if help was called
        return True

    builder = NuttXBuilder(ctx.confpath)
    new_conf = None
    if builder.need_build():
        builder.build_all()
        if not ctx.noflash:
            builder.flash_all()
        new_conf = builder.new_conf()

    # exit now when build only mode
    if ctx.buildonly:
        return True

    if new_conf:
        cfg = EnvConfig(new_conf)
    else:
        cfg = EnvConfig(ctx.confpath)

    pt = MyPytest(cfg, ctx.ignorefile, ctx.exitonfail, ctx.verbose)

    if ctx.runcollect:
        collect_run(pt, ctx)

    if ctx.runtest:
        test_run(pt, ctx)

    return True


###############################################################################
# Function: click_final_init
###############################################################################


def click_final_init() -> None:
    """Handle final Click initialization."""
    # add interfaces
    for cmd in commands_list:
        main.add_command(cmd)


# final click initialization
click_final_init()
