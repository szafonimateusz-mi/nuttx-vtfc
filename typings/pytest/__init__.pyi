# SPDX-License-Identifier: Apache-2.0
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""Typing stub for pytest module."""

from typing import Any, Dict, List

from ntfc.product import Product
from ntfc.products import ProductsHandler

# Custom pytest attributes added by NTFC
testroot: str
testpath: str
result_dir: str
ntfcyaml: Dict[str, Any]
product: ProductsHandler
task: Any
cfgtest: Dict[str, Any]
products: List[Product]

# Allow access to all standard pytest attributes
def __getattr__(name: str) -> Any: ...
