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

"""Host-based QEMU implementation."""

from typing import TYPE_CHECKING

from .host import DeviceHost

if TYPE_CHECKING:
    from ntfc.coreconfig import CoreConfig

##############################################################################
# Class: DeviceQemu
###############################################################################


class DeviceQemu(DeviceHost):
    """This class implements host-based QEMU emulator."""

    def __init__(self, conf: "CoreConfig"):
        """Initialize QEMU emulator device."""
        DeviceHost.__init__(self, conf)

    def start(self) -> None:
        """Start QEMU emulator."""
        elf = self._conf.elf_path
        exec_path = self._conf.exec_path
        exec_args = self._conf.exec_args

        if not elf:
            raise IOError
        if not exec_path:
            raise KeyError("no exec_path in configuration file!")

        cmd = []
        uptime = self._conf.uptime
        kernel_param = "-kernel " + elf

        cmd.append(exec_path)
        cmd.append(" ")
        cmd.append(exec_args)
        cmd.append(" ")
        cmd.append(kernel_param)

        # open host-based emulation
        self.host_open(cmd, uptime)

    @property
    def name(self) -> str:
        """Get device name."""
        return "qemu"
