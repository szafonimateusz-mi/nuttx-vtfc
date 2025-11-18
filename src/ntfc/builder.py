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

"""Build manager for NuttX configuration."""

import os
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Union

import yaml

from ntfc.logger import logger


class NuttXBuilder:
    """NuttX configuration builder (CMake only)."""

    def __init__(self, yaml_cfg: Union[str, Dict]):
        """Initialize NuttX builder."""
        if isinstance(yaml_cfg, str):
            self._load_config(yaml_cfg)
        elif isinstance(yaml_cfg, dict):
            self._cfg_values = yaml_cfg
        else:
            raise TypeError("invalid config file type")

    def _load_config(self, yaml_path: str) -> None:  # pragma: no cover
        """Load configuration."""
        with open(yaml_path, "r") as f:
            self._cfg_values = yaml.safe_load(f)

    def _run_command(
        self, cmd: List[str], check: bool, env: Any
    ) -> None:  # pragma: no cover
        """Run command."""
        subprocess.run(cmd, check=True, env=env)

    def _make_dir(self, path: Path) -> None:
        """Create dir."""
        os.makedirs(path, exist_ok=True)

    def _run_cmake(
        self,
        source: str,
        build: str,
        generator: str = "Ninja",
        defines: Dict[str, str] = None,
        env: str = None,
    ):
        """Run CMake configure step."""
        build_path = Path(build)
        self._make_dir(build_path)

        # base command
        cmd = [
            "cmake",
            f"-B{build}",
            f"-S{source}",
            f"-G{generator}",
        ]

        # add -DVAR=value parameters
        if defines:  # pragma: no cover
            for k, v in defines.items():
                cmd.append(f"-D{k}={v}")

        # merge environment variables
        run_env = os.environ.copy()
        if env:
            run_env.update(env)  # pragma: no cover

        self._run_command(cmd, check=True, env=run_env)

    def _run_build(self, build: str, env: str = None):
        """Run the CMake build step."""
        build = Path(build)

        cmd = [
            "cmake",
            "--build",
            build,
        ]

        run_env = os.environ.copy()
        if env:
            run_env.update(env)  # pragma: no cover

        self._run_command(cmd, check=True, env=run_env)

    def _build_core(self, core, cores, product):
        """Build single core image."""
        if "defconfig" in cores[core]:
            build_dir = (
                product
                + "-"
                + self._cfg_values[product]["name"]
                + "-"
                + cores[core]["name"]
            )

            cfg_build_dir = self._cfg_values["config"].get("build_dir", None)
            if not cfg_build_dir:  # pragma: no cover
                print("ERROR: not found build_dir in YAML configuration!")
                exit(1)

            cfg_cwd = self._cfg_values["config"].get("cwd", None)
            if not cfg_cwd:  # pragma: no cover
                print("ERROR: not found cwd in YAML configuration!")
                exit(1)

            build_path = os.path.join(cfg_build_dir, build_dir)
            build_cfg = cores[core]["defconfig"]
            logger.info(
                f"build image " f"conf: {build_cfg}, out: {build_path}"
            )

            nuttx_dir = os.path.join(cfg_cwd, "nuttx")

            # configure build
            self._run_cmake(
                source=nuttx_dir,
                build=build_path,
                generator="Ninja",
                defines={"BOARD_CONFIG": build_cfg},
            )

            # build
            self._run_build(build_path)

            # add elf and conf path
            cores[core]["elf_path"] = os.path.join(build_path, "nuttx")
            cores[core]["conf_path"] = os.path.join(build_path, ".config")

    def _flash_core(self, core, cores):  # pragma: no cover
        """Flash single core image."""
        flash_cmd = cores[core].get("flash", None)
        if flash_cmd:
            cmd = flash_cmd.split()
            img_path = Path(cores[core]["elf_path"])

            cmd.append(str(img_path.parent) + "/nuttx.hex")
            logger.info(f"flash image cmd: {cmd}")
            self._run_command(cmd, True, None)

    def need_build(self) -> bool:
        """Check if we need build something."""
        for product in self._cfg_values:
            if "product" in product:
                cores = self._cfg_values[product]["cores"]
                for core in cores:
                    if cores[core].get("defconfig", None):
                        return True
        return False

    def build_all(self) -> None:
        """Build all defconfigs from configuration file."""
        for product in self._cfg_values:
            if "product" in product:
                cores = self._cfg_values[product]["cores"]
                for core in cores:
                    self._build_core(core, cores, product)

    def flash_all(self) -> None:
        """Flash all available images."""
        for product in self._cfg_values:
            if "product" in product:
                cores = self._cfg_values[product]["cores"]
                for core in cores:
                    self._flash_core(core, cores)

    def new_conf(self) -> Dict:
        """Get modified YAML config."""
        return self._cfg_values
