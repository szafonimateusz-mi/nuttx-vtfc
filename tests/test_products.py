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

from ntfc.products import ProductsHandler


def test_products_init_inval():

    with patch("ntfc.product.Product") as mockdevice:

        dev = mockdevice.return_value
        products = [dev, dev]

        h = ProductsHandler(products)

        dev.sendCommand.return_value = 0
        assert h.sendCommand("") == 0
        dev.sendCommand.return_value = 1
        assert h.sendCommand("") == 1

        dev.sendCommandReadUntilPattern.return_value = 0
        assert h.sendCommandReadUntilPattern("") == 0
        dev.sendCommandReadUntilPattern.return_value = 1
        assert h.sendCommandReadUntilPattern("") == 1

        assert h.sendCtrlCmd("Z") is None

        dev.busyloop = False
        assert h.busyloop is False
        dev.busyloop = True
        assert h.busyloop is True

        dev.crash = False
        assert h.crash is False
        dev.crash = True
        assert h.crash is True

        dev.notalive = False
        assert h.notalive is False
        dev.notalive = True
        assert h.notalive is True

        dev.reboot.return_value = True
        assert h.reboot() is True
        dev.reboot.return_value = False
        assert h.reboot() is True
