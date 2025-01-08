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

from ntfc.testfilter import FilterTest


def mock_extract_test_requirements1(item):
    return ([], [], [])


def mock_extract_test_requirements2(item):
    return (["CMD1", "CMD2"], ["CONFIG1", "CONFIG2"], ["EXTRA1", "EXTRA2"])


def test_filterest_filter():

    with patch("ntfc.envconfig.EnvConfig") as mockdevice:
        config = mockdevice.return_value

        f = FilterTest(config)

        f.extract_test_requirements = mock_extract_test_requirements1
        skip, reason = f.check_test_support(None)
        assert skip is False
        assert reason is None

        config.kv_check.return_value = False
        config.cmd_check.return_value = False
        config.extra_check.return_value = False
        f.extract_test_requirements = mock_extract_test_requirements2
        skip, reason = f.check_test_support(None)
        assert skip is True
        assert reason == "Required config 'CONFIG1' not enabled"

        config.kv_check.return_value = True
        config.cmd_check.return_value = False
        config.extra_check.return_value = False
        f.extract_test_requirements = mock_extract_test_requirements2
        skip, reason = f.check_test_support(None)
        assert skip is True
        assert reason == "Required symbol 'CMD1' not found in ELF"

        config.kv_check.return_value = True
        config.cmd_check.return_value = True
        config.extra_check.return_value = False
        f.extract_test_requirements = mock_extract_test_requirements2
        skip, reason = f.check_test_support(None)
        assert skip is True
        assert reason == "Extra parameter 'EXTRA1' not found"
