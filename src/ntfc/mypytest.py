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
from ntfc.pytest.configure import PytestConfigPlugin

if TYPE_CHECKING:
    from ntfc.device.common import DeviceCommon

    from .envconfig import EnvConfig

# required for plugin
hookimpl = HookimplMarker("pytest")


###############################################################################
# Class: _RunnerPlugin
###############################################################################


class _RunnerPlugin:
    def __init__(self, nologs: bool = False) -> None:
        """Initialize custom pytest test runner plugin."""
        self._logs: Dict[Dict[str, Any]] = {}
        self._nologs = nologs

    def _collect_device_logs_teardown(self) -> None:
        """Teardown for device log."""
        # stop device log collector
        if self._nologs:
            return

        i = 0
        for product in pytest.products:
            name = "product" + str(i)
            product.stop_log_collect()
            # close files
            self._logs[name]["console"].close()
            i += 1

    def _collect_device_logs(self, request) -> None:
        """Initiate device log writing into a new test file."""
        if self._nologs:
            return

        testname = request.node.name

        i = 0
        for product in pytest.products:
            name = "product" + str(i)
            product_dir = os.path.join(pytest.result_dir, name)

            if name not in self._logs:
                os.makedirs(product_dir, exist_ok=True)
                self._logs[name] = {}

            # open log files
            tmp = os.path.join(product_dir, testname + ".console.txt")
            self._logs[name]["console"] = open(tmp, "a")
            # start device log collector
            product.start_log_collect(self._logs[name])
            i += 1

    @pytest.fixture(scope="function", autouse=True)
    def prepare_test(self, request) -> None:
        """Prepare test case."""
        # initialize log collector
        self._collect_device_logs(request)
        # register log collector teardown
        request.addfinalizer(self._collect_device_logs_teardown)

    @pytest.fixture
    def switch_to_core(self) -> None:
        pass  # pragma: no cover

    @pytest.fixture
    def core(self) -> None:
        pass  # pragma: no cover


###############################################################################
# Class: _CollectedItem
###############################################################################


class _CollectedItem:
    def __init__(
        self,
        directory: str,
        module: str,
        name: str,
        path: str,
        line: int,
        nodeid: str,
        root: str,
    ) -> None:
        """Initialzie collection item."""
        self._directory = directory
        self._module = module
        self._name = name
        self._path = path
        self._line = line
        self._nodeid = nodeid
        self._module2 = (
            root
            + "_"
            + "_".join(part.capitalize() for part in module.split("/")[:-1])
        )

    def __str__(self) -> str:
        """Get collected item string representation."""
        _str = "CollectedItem: " + self.name
        return _str

    @property
    def module2(self) -> str:
        """Get collected module name (short version)."""
        return self._module2

    @property
    def directory(self) -> str:
        """Get collected item directory."""
        return self._directory

    @property
    def module(self) -> str:
        """Get collected item module."""
        return self._module

    @property
    def name(self) -> str:
        """Get collected item name."""
        return self._name

    @property
    def path(self) -> str:
        """Get collected item file."""
        return self._path

    @property
    def line(self) -> int:
        """Get collected item line."""
        return self._line

    @property
    def nodeid(self) -> str:
        """Get collected item node ID."""
        return self._nodeid


###############################################################################
# Class: _Collected
###############################################################################


class _Collected:
    def __init__(
        self,
        items: List[_CollectedItem],
        skipped: List[Tuple[pytest.Item, str]],
    ):
        """Initialize test collected data."""
        self._items = items
        self._skipped = skipped
        self._modules = self._get_modules()

    def _get_modules(self) -> List[str]:
        """Get collected modules."""
        mod = set()
        for i in self._items:
            mod.add(i.module2)
        return list(mod)

    @property
    def items(self) -> List[_CollectedItem]:
        """Get collected items."""
        return self._items

    @property
    def skipped(self) -> List[Tuple[pytest.Item, str]]:
        """Get skipped items."""
        return self._skipped

    @property
    def modules(self) -> List[str]:
        """Get collected modules."""
        return self._modules


###############################################################################
# Class: _CollectorPlugin
###############################################################################


class _CollectorPlugin:
    def __init__(self) -> None:
        """Initialize custom pytest collector plugin."""
        self.collected_items: List[Tuple[Any, Any]] = []
        self.parsed_items: List[_CollectedItem] = []

    @property
    def parsed(self) -> List[_CollectedItem]:
        """Get collected items in parsed format."""
        return self.parsed_items

    def pytest_runtestloop(self, session: pytest.Session) -> bool:
        """Prevent tests from running.

        Returning True stops test execution.
        """
        return True

    def pytest_collection_finish(self, session: pytest.Session) -> None:
        """Pytest collection finish callback."""
        self.collected_items.extend(session.items)

        # extract useful data from items
        for item in session.items:
            path, lineno, name = item.location
            abs_path = os.path.abspath(path)
            directory = os.path.dirname(abs_path)
            module = path.replace(pytest.testpath, "")

            ci = _CollectedItem(
                directory,
                module,
                name,
                abs_path,
                lineno,
                item.nodeid,
                pytest.ntfcyaml["module"],
            )
            self.parsed_items.append(ci)


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
        runner = _RunnerPlugin(nologs)

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
        collector = _CollectorPlugin()

        # run pytest with our custom collector plugin
        self._run([testpath], [collector])

        collected = _Collected(collector.parsed, self._ptconfig.skipped_items)

        # return parsed items and skipped
        return collected
