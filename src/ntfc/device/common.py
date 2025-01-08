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

"""Device common interface."""

from abc import ABC, abstractmethod
from dataclasses import astuple, dataclass
from enum import IntEnum
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    import re

###############################################################################
# Class: CmdStatus
###############################################################################


class CmdStatus(IntEnum):
    """Command status."""

    SUCCESS = 0
    NOTFOUND = -1
    TIMEOUT = -2

    def __str__(self):
        """Return enum string."""
        return self.name


###############################################################################
# Class: CmdReturn
###############################################################################


@dataclass
class CmdReturn:
    """Command return data."""

    status: CmdStatus
    rematch: "Optional[re.Match]" = None
    output: str = ""

    def valid_match(self):
        """Check if RE match is valid."""
        return (self.status == CmdStatus.SUCCESS) and self.rematch

    def __iter__(self):
        """Make the dataclass instance iterable."""
        for value in astuple(self):
            yield value


###############################################################################
# Class: DeviceCommon
###############################################################################


class DeviceCommon(ABC):
    """Device common interface."""

    @abstractmethod
    def start(self) -> None:
        """Start device."""

    @abstractmethod
    def send_cmd_read_until_pattern(
        self, cmd: bytes, pattern: bytes, timeout: int
    ) -> CmdReturn:
        """Send command to device and read until the specified pattern."""

    @abstractmethod
    def send_ctrl_cmd(self, ctrl_char: str) -> CmdStatus:
        """Send control command to the device."""

    @abstractmethod
    def name(self) -> str:
        """Get device name."""

    @abstractmethod
    def prompt(self) -> str:
        """Return target device prompt."""

    @abstractmethod
    def no_cmd(self) -> str:
        """Return command not found string."""

    @abstractmethod
    def busyloop(self) -> bool:
        """Check if the device is in busy loop."""

    @abstractmethod
    def crash(self) -> bool:
        """Check if the device is crashed."""

    @abstractmethod
    def notalive(self) -> bool:
        """Check if the device is dead."""

    @abstractmethod
    def poweroff(self):
        """Poweroff the device."""

    @abstractmethod
    def reboot(self, timeout: int) -> bool:
        """Reboot the device."""

    @abstractmethod
    def start_log_collect(self, logs) -> None:
        """Start device log collector."""

    @abstractmethod
    def stop_log_collect(self) -> None:
        """Stop device log collector."""
