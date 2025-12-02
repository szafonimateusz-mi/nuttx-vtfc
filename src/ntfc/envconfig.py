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

"""Configuration handler."""

import pprint
from typing import Dict, List, Union

import yaml

from ntfc.logger import logger
from ntfc.productconfig import ProductConfig


class EnvConfig:
    """This class handles tests environment configuration."""

    def __init__(self, yaml_cfg: Union[str, Dict], args=None) -> None:
        """Initialzie tests environment configuration."""
        self._args = []
        self._cfg_values = {}

        if isinstance(yaml_cfg, str):
            self._load_config(yaml_cfg)
        elif isinstance(yaml_cfg, dict):
            self._cfg_values = yaml_cfg
        else:
            raise TypeError("invalid configuration")

        self._products = self._products_create(self._cfg_values)

        self._print_config()

    def _products_create(self, config: dict) -> List[ProductConfig]:
        """Create product configuration."""
        products = []
        for k in config.keys():
            if "product" in k:
                p = ProductConfig(config[k])
                products.append(p)

        return products

    def _load_config(self, yaml_path: str) -> None:
        """Load configuration."""
        try:
            with open(yaml_path, "r") as f:
                self._cfg_values = yaml.safe_load(f)

        except FileNotFoundError:
            logger.error(f"ERROR: Configuration file not found: {yaml_path}")
            exit(1)

    def _print_config(self) -> None:
        """Print device configuration."""
        print("YAML config:")
        pp = pprint.PrettyPrinter()
        pp.pprint(self._cfg_values)

    @property
    def common(self) -> Dict:
        """Return device parameters."""
        return self._cfg_values.get("config", {})

    @property
    def product(self) -> list:
        """Return product instance."""
        return self._products

    def product_get(self, product: int = 0) -> dict:
        """Return product parameters."""
        if product >= len(self._products):
            return None
        return self._products[product].config

    def core(self, product: int = 0, cpu: int = 0) -> Dict:
        """Return core parameters."""
        if product >= len(self._products):
            return ""
        return self._products[product].core(cpu)

    @property
    def config(self) -> Dict:
        """Return test configuration."""
        return self._cfg_values

    # dep_config
    def kv_check(self, cfg: str, product: int = 0, core: int = 0) -> bool:
        """Check Kconfig option."""
        return self._products[product].kv_check(cfg, core)

    def cmd_check(self, cmd: str, product: int = 0, core: int = 0) -> bool:
        """Check if command is available in binary."""
        product = 0
        return self._products[product].cmd_check(cmd, core)

    def extra_check(self, extra: str, product: int = 0, core: int = 0) -> bool:
        """Check for extra options."""
        # not supported yet
        return False
