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

import time

import pytest
from pexpect.exceptions import ExceptionPexpect

from ntfc.device.host import DeviceHost


# need to define start which is specific for device implementation
class DeviceHost2(DeviceHost):
    def start(self):
        pass


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


def mock_send_command_long_response0(timeout=1):
    return b"DUMMY"


g_mock_send_command_long_response1_cntr = 0


def mock_send_command_long_response1(timeout=1):
    global g_mock_send_command_long_response1_cntr
    g_mock_send_command_long_response1_cntr += 1

    if g_mock_send_command_long_response1_cntr == 1:
        return b""
    elif g_mock_send_command_long_response1_cntr == 2:
        return b""
    elif g_mock_send_command_long_response1_cntr == 3:
        return b""
    elif g_mock_send_command_long_response1_cntr == 4:
        return b"Dxxx"
    else:
        return b""


g_mock_send_command_long_response2_cntr = 0


def mock_send_command_long_response2(timeout=1):
    global g_mock_send_command_long_response2_cntr
    g_mock_send_command_long_response2_cntr += 1

    if g_mock_send_command_long_response2_cntr == 1:
        return b""
    elif g_mock_send_command_long_response2_cntr == 2:
        return b""
    elif g_mock_send_command_long_response2_cntr == 3:
        return b""
    elif g_mock_send_command_long_response2_cntr == 4:
        return b"DUMMY"
    else:
        return b""


g_mock_send_command_long_response3_cntr = 0


def mock_send_command_long_response3(timeout=1):
    global g_mock_send_command_long_response3_cntr
    g_mock_send_command_long_response3_cntr += 1

    if g_mock_send_command_long_response3_cntr == 1:
        return b""
    elif g_mock_send_command_long_response3_cntr == 2:
        return b""
    elif g_mock_send_command_long_response3_cntr == 3:
        return b"D"
    elif g_mock_send_command_long_response3_cntr == 4:
        return b""
    elif g_mock_send_command_long_response3_cntr == 5:
        return b""
    elif g_mock_send_command_long_response3_cntr == 6:
        return b"U"
    else:
        return b""


def mock_send_command_long_response4(timeout=1):
    global g_mock_send_command_long_response4_cntr
    g_mock_send_command_long_response4_cntr += 1

    if g_mock_send_command_long_response4_cntr == 1:
        return b""
    elif g_mock_send_command_long_response4_cntr == 2:
        return b""
    elif g_mock_send_command_long_response4_cntr == 3:
        return b"D"
    elif g_mock_send_command_long_response4_cntr == 4:
        return b""
    elif g_mock_send_command_long_response4_cntr == 5:
        return b""
    elif g_mock_send_command_long_response4_cntr == 6:
        return b"U"
    elif g_mock_send_command_long_response4_cntr == 7:
        return b"MMY"
    else:
        return b""


def test_device_host_command_long_time():

    global g_mock_send_command_long_response1_cntr
    global g_mock_send_command_long_response2_cntr
    global g_mock_send_command_long_response3_cntr
    global g_mock_send_command_long_response4_cntr

    conf = {}
    path = "./tests/resources/nuttx/sim/nuttx"
    dev = DeviceHost2(conf)

    # open executable
    ret = dev.host_open([path])
    assert ret is not None
    assert dev.notalive is False

    # check response time when data are ready in the first read
    dev._read_all = mock_send_command_long_response0
    now_time = time.time()
    timeout = 5
    ret = dev.send_cmd_read_until_pattern(b"dummy", b"DUMMY", timeout)
    assert ret.status == 0
    assert time.time() - now_time < timeout

    # send command with long response time - timeout
    g_mock_send_command_long_response1_cntr = 0
    dev._read_all = mock_send_command_long_response1
    now_time = time.time()
    timeout = 5
    ret = dev.send_cmd_read_until_pattern(b"dummy", b"DUMMY", timeout)
    assert ret.status == -2
    assert time.time() - now_time > timeout

    # send command with long response time
    g_mock_send_command_long_response2_cntr = 0
    dev._read_all = mock_send_command_long_response2
    timeout = 5
    ret = dev.send_cmd_read_until_pattern(b"dummy", b"DUMMY", timeout)
    assert ret.status == 0

    # send command with long response time - timeout
    g_mock_send_command_long_response3_cntr = 0
    dev._read_all = mock_send_command_long_response3
    now_time = time.time()
    timeout = 1
    ret = dev.send_cmd_read_until_pattern(b"dummy", b"DUMMY", timeout)
    assert ret.status == -2
    assert time.time() - now_time > timeout

    # send command with long response time
    g_mock_send_command_long_response4_cntr = 0
    dev._read_all = mock_send_command_long_response4
    timeout = 1
    ret = dev.send_cmd_read_until_pattern(b"dummy", b"DUMMY", timeout)
    assert ret.status == 0
