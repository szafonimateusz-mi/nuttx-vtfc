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

from unittest.mock import patch

import pytest

from ntfc.device.qemu import DeviceQemu


def host_open_dummy(cmd, uptime):
    assert uptime == 3
    assert cmd == ["some/path", " ", "some args", " ", "-kernel some/path"]


def test_device_qemu_open():

    with patch("ntfc.coreconfig.CoreConfig") as mockdevice:
        config = mockdevice.return_value

        config.exec_path = ""
        config.exec_args = ""
        config.elf_path = ""

        qemu = DeviceQemu(config)

        with pytest.raises(IOError):
            qemu.start()

        config.exec_path = ""
        config.exec_args = ""
        config.elf_path = "some/path"

        with pytest.raises(KeyError):
            qemu.start()

        assert qemu.name == "qemu"

        qemu.host_open = host_open_dummy

        config.exec_path = "some/path"
        config.exec_args = "some args"
        config.elf_path = "some/path"
        config.uptime = 3

        qemu.start()
