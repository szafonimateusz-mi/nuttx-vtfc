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

import pytest

from ntfc.builder import NuttXBuilder

conf_dir = {
    "config": {"cwd": "aaa", "build_dir": "bbb"},
    "product": {
        "name": "xxx",
        "cores": {
            "core0": {
                "name": "dummy",
                "device": "sim",
            }
        },
    },
}


def builder_run_command_dummy(cmd, env):
    pass


def builder_make_dir_dummy(path):
    pass


def test_builder_init():

    with pytest.raises(TypeError):
        _ = NuttXBuilder(None)

    b = NuttXBuilder(conf_dir)

    assert b.need_build() is False

    conf_dir["product"]["cores"]["core0"]["defconfig"] = "dummy/path"
    assert b.need_build() is True

    b._run_command = builder_run_command_dummy
    b._make_dir = builder_make_dir_dummy

    b.build_all()

    new_confg = b.new_conf()
    assert new_confg is not None

    assert (
        new_confg["product"]["cores"]["core0"]["elf_path"]
        == "bbb/product-xxx-dummy/nuttx"
    )
    assert (
        new_confg["product"]["cores"]["core0"]["conf_path"]
        == "bbb/product-xxx-dummy/.config"
    )
