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

"""Products handler class implementation."""

from typing import TYPE_CHECKING, List, Optional, Union

from ntfc.logger import logger

if TYPE_CHECKING:
    from ntfc.device.common import CmdReturn, CmdStatus
    from ntfc.product import Product

###############################################################################
# Class: ProductsHandler
###############################################################################


class ProductsHandler:
    """This class implements work-around to run all products at once.

    It can be useful to run tests for many DTU at once.
    This implementation is not the best, it needs to be done better
    in the future.
    """

    def __init__(self, products: List["Product"]):
        """Initialize all products handler."""
        self._products = products

    def sendCommand(  # noqa: N802
        self,
        cmd: str,
        expects: Optional[Union[str, List[str]]] = None,
        args: Optional[Union[str, List[str]]] = None,
        timeout: int = 30,
        flag: str = "",
        match_all: bool = True,
        regexp: bool = False,
    ) -> "CmdStatus":
        """Send command to all products."""
        for p in self._products:
            ret = p.sendCommand(
                cmd, expects, args, timeout, flag, match_all, regexp
            )
            if ret != 0:
                logger.info(f"sendCommand failed for product {p}")
                return ret

        return 0

    def sendCommandReadUntilPattern(  # noqa: N802
        self,
        cmd: str,
        pattern: Optional[Union[str, bytes, List[Union[str, bytes]]]] = None,
        args: Optional[Union[str, List[str]]] = None,
        timeout: int = 30,
    ) -> "CmdReturn":
        """Send command to all products."""
        for p in self._products:
            ret = p.sendCommandReadUntilPattern(cmd, pattern, args, timeout)
            if ret != 0:
                logger.info(
                    f"sendCommandReadUntilPattern failed for product {p}"
                )
                return ret

        return 0

    def sendCtrlCmd(self, ctrl_char: str) -> None:  # noqa: N802
        """Send ctrl command to all products."""
        for p in self._products:
            p.sendCtrlCmd(ctrl_char)

    @property
    def busyloop(self) -> bool:
        """Get busyloop flag from products."""
        for p in self._products:
            if p.busyloop:
                logger.info(f"busyloop for product {p}")
                return True
        return False

    @property
    def crash(self) -> bool:
        """Get crash flag from products."""
        for p in self._products:
            if p.crash:
                logger.info(f"crash for product {p}")
                return True
        return False

    @property
    def notalive(self) -> bool:
        """Get notalive flag from products."""
        for p in self._products:
            if p.notalive:
                logger.info(f"notalive for product {p}")
                return True
        return False

    def reboot(self) -> bool:
        """Run reboot for all products."""
        for p in self._products:
            if not p.reboot():
                logger.info(f"reboot failed for product {p}")
        return True

    @property
    def cur_name(self) -> str:
        """Get current product."""
        # TODO: many products not supported yet
        return self._products[0].name

    @property
    def cur_core(self) -> str:
        """Get current core."""
        # TODO: many products not supported yet
        return self._products[0].cur_core
