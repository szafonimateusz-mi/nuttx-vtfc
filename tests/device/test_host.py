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
from pexpect.exceptions import ExceptionPexpect

from ntfc.device.host import DeviceHost


# need to define start which is specific for device implementation
class DeviceHost2(DeviceHost):
    def start(self):
        pass

    def _dev_is_health_priv(self):
        return True


def test_device_host_open():

    conf = {}
    path = "./tests/resources/nuttx/sim/nuttx"
    dev = DeviceHost2(conf)

    with pytest.raises(IOError):
        dev.host_close()

    assert dev.notalive is True

    with pytest.raises(ExceptionPexpect):
        dev.host_open(["dummyxxxx"])

    assert dev.notalive is True

    # open executable
    ret = dev.host_open([path])
    assert ret is not None
    assert dev.notalive is False

    # close executable
    dev.host_close()
    assert dev.notalive is True


def test_device_host_command():

    conf = {}
    path = "./tests/resources/nuttx/sim/nuttx"
    dev = DeviceHost2(conf)

    # open executable
    ret = dev.host_open([path])
    assert ret is not None
    assert dev.notalive is False

    # check hello world command in bytes
    ret = dev.send_command(b"hello", 1)
    assert b"Hello, World!" in ret

    # check hello world command in string
    ret = dev.send_command("hello", 1)
    assert b"Hello, World!" in ret

    # no pattern in output
    ret = dev.send_cmd_read_until_pattern(b"hello", b"dummy", 1)
    assert ret.status == -2

    # pattern in output
    ret = dev.send_cmd_read_until_pattern(b"hello", b"Hello", 1)
    assert ret.status == 0

    # pattern in output
    ret = dev.send_cmd_read_until_pattern(b"hello", b"World!", 1)
    assert ret.status == 0

    # pattern in output
    ret = dev.send_cmd_read_until_pattern(b"hello", b"Hello, World!", 1)
    assert ret.status == 0


# TODO: more tests for host device !!!!
#   - test for timeout
#   - test for very long output
#   - test for
