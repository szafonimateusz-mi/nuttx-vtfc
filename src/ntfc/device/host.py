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

"""Host-based emulated devices."""

import os
import signal
import time
from typing import TYPE_CHECKING, List, Optional

import pexpect
import psutil

from ntfc.logger import logger

from .common import DeviceCommon

if TYPE_CHECKING:
    from ntfc.envconfig import ProductConfig

###############################################################################
# Class: DeviceHost
###############################################################################


class DeviceHost(DeviceCommon):
    """This class implements common interface for host emulated devices."""

    def __init__(self, conf: "ProductConfig"):
        """Initialize host based device.

        :param conf: configuration handler
        """
        DeviceCommon.__init__(self, conf)
        self._child = None
        self._cwd = None
        self._cmd: Optional[List[str]] = None

    def _dev_is_health_priv(self) -> bool:
        """Check if the host device is OK."""
        if not self._child:
            return False

        if not self._child.isalive():
            return False

        return True

    def _dev_reopen(self) -> pexpect.spawn:
        """Reopen host device."""
        if not self._cmd:
            raise ValueError("Host open command is empty")

        self.host_close()

        return self.host_open(self._cmd)

    def _write(self, data: bytes) -> None:
        """Write to the host device."""
        if not self.dev_is_health():
            return

        # send char by char to avoid line length full
        for c in data:
            self._child.send(bytes([c]))

        # add new line if missing
        if data[-1] != ord("\n"):
            self._child.send(b"\n")

    def _write_ctrl(self, c: str) -> None:
        """Write a control character to the host device."""
        if not self.dev_is_health():
            return

        self._child.sendcontrol(c)

    def _read(self) -> bytes:  # pragma: no cover
        """Read data from the host device."""
        if not self.dev_is_health():
            return b""

        try:
            return self._child.read_nonblocking(size=1024, timeout=0)

        except pexpect.TIMEOUT:
            return b""

        except pexpect.EOF:
            return b""

        except BaseException:
            raise

    def _kill_process_group(self, process: pexpect.spawn) -> None:
        """Kill process group."""
        pid = process.pid

        # terminate process gracefully
        os.killpg(pid, signal.SIGTERM)

        try:
            # wait for the process group to terminate
            parent = psutil.Process(pid)
            parent.wait(timeout=10)
            logger.info(f"Process group {pid} terminated successfully.")

        except psutil.TimeoutExpired:  # pragma: no cover
            logger.warning(
                f"Timeout: Process group {pid}"
                "did not terminate within 5 seconds."
            )
            # force termination
            os.killpg(pid, signal.SIGKILL)
            logger.info(f"Sent SIGKILL to process group {pid}")

        self._child = None

    def host_open(self, cmd: List[str], uptime: int = 0) -> pexpect.spawn:
        """Open host-based target device."""
        if self._child:
            raise IOError("Host device already open")

        self._child = None
        self.clear_fault_flags()

        # we need command to reopen file in the case of crash
        self._cmd = cmd

        logger.info("spawn cmd: {}".format("".join(cmd)))
        print("spawn cmd: {}".format("".join(cmd)))
        self._child = pexpect.spawn(
            "".join(cmd), timeout=10, maxread=20000, cwd=self._cwd
        )

        time.sleep(uptime)

        ret = self._wait_for_boot()
        if ret is False:  # pragma: no cover
            raise TimeoutError("device boot timeout")

        return self._child

    def host_close(self) -> None:
        """Close host-based target device."""
        if not self._child:
            raise IOError("Host device not ready")

        if self._child.isalive():
            # send power off
            self.poweroff()
            time.sleep(1)

        if self._child.isalive():
            # kill process group
            self._kill_process_group(self._child)

        self._child = None

        logger.info("host device closed")

    @property
    def name(self) -> str:
        """Get device name."""
        return "host_unknown"

    @property
    def notalive(self) -> bool:
        """Check if the device is dead."""
        if not self._child:
            return True
        return not self._child.isalive()

    def poweroff(self) -> None:
        """Poweroff the device."""
        self.send_command(self._dev.poweroff_cmd)

    def reboot(self, timeout: int) -> bool:
        """Reboot the device."""
        return True if self._dev_reopen() else False
