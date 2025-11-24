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

"""NTFC plugin for pytest."""

import os
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

import pytest
import yaml
from pluggy import HookimplMarker

from ntfc.device.getdev import get_device
from ntfc.logger import logger
from ntfc.product import Product

from .collector import Collected, CollectorPlugin
from .configure import PytestConfigPlugin
from .runner import RunnerPlugin

if TYPE_CHECKING:
    from ntfc.device.common import DeviceCommon

    from .envconfig import EnvConfig

# required for plugin
hookimpl = HookimplMarker("pytest")


###############################################################################
# Class: MyPytest
###############################################################################


class MyPytest:
    """Custom wrapper for pytest."""

    def __init__(
        self,
        config: "EnvConfig",
        ignorepath: Optional[str] = None,
        exit_on_fail: bool = False,
        verbose: bool = False,
        device: Optional[List["DeviceCommon"]] = None,
    ) -> None:
        """Initialize pytest wrapper.

        :param config: configuration instance
        :param exit_on_fail: exit on first test fail if set to True
        :param verbose: verbose output if set to True
        """
        self._config = config
        self._device = device
        self._opt = []
        self._plugins = []
        self._cfg_module = {}

        if exit_on_fail:
            self._opt.append("-x")

        if verbose:
            self._opt.append("-qq")

        # ignore tests
        if ignorepath:
            self.ignore_tests(ignorepath)

        # configure plugin
        hookimpl_marker = hookimpl(hookwrapper=True)
        hookimpl_marker(
            PytestConfigPlugin.__dict__["pytest_runtest_makereport"]
        )
        self._ptconfig = PytestConfigPlugin(config)

        # add our custom pytest plugin
        self._plugins.append(self._ptconfig)

    def _create_products(
        self, config: "EnvConfig", device: Optional[List["DeviceCommon"]]
    ) -> List[Product]:
        """Create products according to configuration."""
        tmp = []
        for i in range(len(config.product)):
            if not device or not device[i]:
                dev = get_device(config.product[i])
            else:
                dev = device[i]

            p = Product(dev, config.product[i])
            tmp.append(p)

        return tmp

    def _get_product(self, product: int = 0) -> Dict[str, str]:
        """Get product configuration."""
        return pytest.products[product]

    def _run(self, extra_opt: List[str], extra_plugins: List[Any]) -> int:
        """Run pytest.

        :param extra_opt:
        :param extra_plugins:
        """
        # get default options and plugins
        opt = self._opt[:]
        plugins = self._plugins[:]

        # extra options and plugins
        opt.extend(extra_opt)
        plugins.extend(extra_plugins)

        # override tox.ini configuration from package root
        opt.extend(["--override-ini", "addopts="])

        # run pytest in collection-only mode with our custom plugin
        return pytest.main(opt, plugins=plugins)

    def _device_start(self) -> None:
        """Start device to test."""
        for product in pytest.products:
            # start device
            product.device.start()
            # finish product initialization
            product.init()

    def _init_pytest(self, testpath: str) -> None:
        """Initialize pytest environment."""
        # inject some objects into pytest module
        pytest.products = self._create_products(self._config, self._device)
        pytest.product = self._get_product(product=0)
        pytest.task = self._config.product_get(product=0)
        pytest.testpath = testpath

        # load per test module configuration
        conf_path = os.path.join(testpath, "ntfc.yaml")
        self._module_config(conf_path)
        pytest.ntfcyaml = self._cfg_module

    def _module_config(self, path) -> None:
        """Load test module configuration."""
        try:
            logger.info(f"ntfc.conf file {path}")
            _path = Path(path)

            with open(_path) as f:  # pragma: no cover
                self._cfg_module = yaml.safe_load(f)

        except TypeError:  # pragma: no cover
            pass

        except NotADirectoryError:
            logger.info("no ntfc.conf file")
            pass

        except FileNotFoundError:
            logger.info("no ntfc.conf file")
            pass

        # module default config
        if "module" not in self._cfg_module:
            self._cfg_module["module"] = "Unknown_"
        if "kvreq" not in self._cfg_module:
            self._cfg_module["kvreq"] = [["CONFIG_DEBUG_SYMBOLS", True]]

    def ignore_tests(self, path: str) -> None:
        """Ignore tests specified in $CWD/ignore.txt file."""
        try:
            logger.info(f"ignore file {path}")
            _path = Path(path)

            with open(_path) as f:  # pragma: no cover
                for line in f:
                    if line[0] == "-" and line[1] == "-":
                        self._opt.append(line[:-1])
        except TypeError:  # pragma: no cover
            pass

        except FileNotFoundError:
            logger.info("no ignore file")
            pass

    def runner(
        self, testpath: str, result: Dict[str, str], nologs: bool = False
    ) -> int:
        """Run tests.

        :param testpath: path to test directory
        :param result: result output configuration
        """
        # initialzie pytest env
        self._init_pytest(testpath)

        opt = [testpath]

        if not nologs:  # pragma: no cover
            # create result directory
            result_dir = result.get("resdir", "./result")
            time_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            pytest.result_dir = os.path.join(result_dir, time_now)
            os.makedirs(pytest.result_dir, exist_ok=True)

            # additional reports
            if result.get("html"):
                path = os.path.join(pytest.result_dir, "report.html")
                opt.append(f"--html={path}")
            if result.get("xml"):
                path = os.path.join(pytest.result_dir, "report.xml")
                opt.append(f"--junitxml={path}")
            if result.get("json"):
                path = os.path.join(pytest.result_dir, "report.json")
                opt.append(f"--json={path}")

        # run pytest with our custom test plugin
        runner = RunnerPlugin(nologs)

        # start device before test start
        self._device_start()

        return self._run(opt, [runner])

    def collect(self, testpath: str) -> Tuple[List[Any], List[Any]]:
        """Collect tests.

        :param testpath:
        """
        # initialzie pytest env
        self._init_pytest(testpath)

        # collector plugin
        collector = CollectorPlugin()

        # run pytest with our custom collector plugin
        self._run([testpath], [collector])

        collected = Collected(collector.parsed, self._ptconfig.skipped_items)

        # return parsed items and skipped
        return collected
