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

"""Product configuration handler."""

from typing import Dict

from ntfc.lib.elf.elf_parser import ElfParser
from ntfc.logger import logger


class ProductConfig:
    """Product configuration."""

    def __init__(self, cfg: Dict) -> None:
        """Initialzie product configuration."""
        self._config = cfg

        self._kv_values = []
        self._elf = []

        for core in range(len(self.cores)):
            conf_path = self.core(cpu=core).get("conf_path", None)
            if conf_path:
                # add entry in dict
                self._kv_values.append({})
                # load config values
                self._load_core_config(core)

        if self.cores:
            self._load_elf()

    def _load_core_config(self, core: int) -> None:
        """Load core configuration."""
        with open(self.core(cpu=core)["conf_path"], "r") as f:
            for line in f:
                # ignore all commented lines
                if line[0] != "#" and line[0] != "\n":
                    name = line.split("=")[0]
                    val = line.split("=")[1]

                    # parse option value
                    if val[0] == "y":
                        val = True
                    else:
                        val = val[1:-2]

                    self._kv_values[core][name] = val

    def _load_elf(self) -> None:
        """Load ELF symbols."""
        for core in range(len(self.cores)):
            path = self.core(cpu=core).get("elf_path", None)
            if path:
                elf = ElfParser(path)
            else:
                elf = None

            self._elf.append(elf)

    @property
    def config(self) -> Dict:
        """Return test configuration."""
        return self._config

    @property
    def cores(self) -> Dict:
        """Return product cores configuration."""
        try:
            return self._config["cores"]
        except KeyError:
            logger.error("no cores info in configuration file!")
            return {}

    @property
    def name(self) -> str:
        """Get product name."""
        try:
            return self._config["name"]
        except KeyError:  # pragma: no cover
            logger.error("no product name in configuration file!")
            return "unknown_name"

    def kv_check(self, cfg: str, core=0) -> bool:
        """Check Kconfig option."""
        if not self._kv_values:
            raise AttributeError("no config data")
        if len(self._kv_values) < core or not self._kv_values[core]:
            raise AttributeError(f"no config data for core {core}")

        return (
            self._kv_values[core][cfg]
            if self._kv_values[core].get(cfg)
            else False
        )

    def core(self, cpu: int = 0) -> Dict:
        """Return core parameters."""
        if cpu == 0:
            cpuname = "core0"
        else:
            cpuname = "core" + str(cpu)

        return self.cores.get(cpuname, "")

    def cmd_check(self, cmd: str, core: int = 0) -> bool:
        """Check if command is available in binary."""
        if not self._elf:
            raise AttributeError("no elf data")
        if len(self._elf) < core or not self._elf[core]:
            raise AttributeError(f"no elf data for core {core}")

        symbol_name = f"{cmd}_main" if "cmocka" in cmd else cmd
        return self._elf[core].has_symbol(symbol_name)
