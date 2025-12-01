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

from ntfc.productconfig import ProductConfig


def test_product_config():

    conf = {
        "name": "product",
        "cores": {
            "core0": {
                "name": "dummy",
                "device": "sim",
                "elf_path": "./tests/resources/nuttx/sim/nuttx",
                "conf_path": "./tests/resources/nuttx/sim/kv_config",
                "uptime": 1,
            },
            "core1": {
                "name": "dummy2",
                "device": "sim2",
                "elf_path": "./tests/resources/nuttx/sim/nuttx",
                "conf_path": "./tests/resources/nuttx/sim/kv_config",
                "uptime": 1,
            },
        },
    }

    p = ProductConfig(conf)

    assert p.core(0)["name"] == "dummy"
    assert p.core(0)["device"] == "sim"
    assert p.core(1)["name"] == "dummy2"
    assert p.core(1)["device"] == "sim2"

    with pytest.raises(AttributeError):
        p.key_check("aaa", 3)

    with pytest.raises(AttributeError):
        p.cmd_check("aaa", 3)

    with pytest.raises(AttributeError):
        p.kv_check("aaa", 3)

    conf = {
        "name": "product",
    }

    p = ProductConfig(conf)

    assert p.cores == {}
    with pytest.raises(AttributeError):
        p.key_check("aaa")
    with pytest.raises(AttributeError):
        p.cmd_check("aaa")
    with pytest.raises(AttributeError):
        p.kv_check("aaa")
