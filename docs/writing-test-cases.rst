==================
Writing Test Cases
==================

NTFC supports comprehensive test case development with flexible test discovery
and execution. Test cases are organized in modules with YAML configuration files
defining requirements and metadata.

Test Module Structure
=====================

Each test module directory contains:

.. code-block:: text

   test-module/
   ├── ntfc.yaml              # Module configuration (required)
   ├── conftest.py            # Pytest configuration (optional)
   ├── test_*.py              # Test case files
   ├── subdir/
   │   └── test_*.py          # Nested test cases
   └── ...

Each test function in a module must have a unique name!

Module Configuration (ntfc.yaml)
=================================

Located in the root of each test module directory.

**Structure:**

.. code-block:: yaml

   module: "Nuttx_System"              # Module identifier

   dependencies:                       # Optional: Python dependencies
     - toml

   requirements:                       # NuttX configuration requirements
     - ["CONFIG_DEBUG_SYMBOLS", True]
     - ["CONFIG_SYSTEM_NSH", True]
     - ["CONFIG_INIT_ENTRYPOINT", "nsh_main"]

**Fields:**

- **module**: Unique module identifier. Hierarchical names use underscores (e.g.,
  ``Nuttx_System``)
- **dependencies**: List of Python packages required by test cases
- **requirements**: NuttX configuration requirements. Tests skip if not met.

Configuration Requirements
===========================

Requirements are specified as ``[config_key, expected_value]`` pairs.

**Boolean Requirements:**

.. code-block:: yaml

   requirements:
     - ["CONFIG_DEBUG_SYMBOLS", True]          # CONFIG must be enabled
     - ["CONFIG_DEBUG_FEATURES", False]        # CONFIG must be disabled

**String/Value Requirements:**

.. code-block:: yaml

   requirements:
     - ["CONFIG_INIT_ENTRYPOINT", "nsh_main"]  # CONFIG must equal specific value
     - ["CONFIG_TASK_NAME_SIZE", "32"]         # CONFIG must equal value

**How Requirements Work:**

1. NTFC reads NuttX ``.config`` file from configuration
2. Extracts configuration values
3. Compares against requirements
4. Raise assertion if any requirement not met

**Example:**

Module requires NSH (NuttX Shell) as entry point:

.. code-block:: yaml

   module: "Nuttx_System_Syscall"

   requirements:
     - ["CONFIG_DEBUG_SYMBOLS", True]
     - ["CONFIG_SYSTEM_NSH", True]
     - ["CONFIG_INIT_ENTRYPOINT", "nsh_main"]

If ``.config`` doesn't have all these settings, assertion is raised.

Test Case Organization
======================

Organize test cases by functionality in subdirectories:

.. code-block:: text

   nuttx-testing/
   ├── ntfc.yaml
   ├── arch/
   │   ├── test_pthread.py
   │   └── os/
   │       ├── test_task.py
   │       └── integration/
   │           └── test_syscall.py
   ├── fs/
   │   ├── test_vfs.py
   │   └── test_mount.py
   └── libc/
       └── test_stdio.py

Directory paths determine module hierarchy. For example:

- ``ntfc.yaml`` module: ``Nuttx_System``
- ``arch/test_pthread.py`` -> ``Nuttx_System_Arch``
- ``arch/os/integration/test_syscall.py`` -> ``Nuttx_System_Arch_Os_Integration``

Use this for filtering tests via ``session.json``.

Pytest Configuration (conftest.py)
==================================

``conftest.py`` enables advanced test generation, filtering, and configuration
for test modules. It can use pytest hooks to dynamically generate test cases and
modify test collection.

**Common Uses:**

1. **Dynamic test generation** from ELF symbols (e.g., LTP tests)
2. **Test case filtering** based on blacklists, skip lists, crash lists
3. **Custom timeout management** for specific tests
4. **Test parameter management** (expected outputs, test variations)
5. **Setup/teardown logic** using fixtures

**Key Pytest Hooks:**

.. list-table::
   :header-rows: 1

   * - Hook
     - Purpose
     - Called
   * - ``pytest_generate_tests``
     - Generate parametrized test cases
     - During test collection
   * - ``pytest_collection_modifyitems``
     - Modify collected test items
     - After test collection
   * - ``@pytest.fixture``
     - Define reusable test setup/teardown
     - Before/after tests

Test Case Patterns
===================

NTFC supports multiple test case patterns.

Simple Command Test
--------------------

Execute NSH command and verify output:

.. code-block:: python

   import pytest

   @pytest.mark.cmd_check("test_main")
   def test_simple():
       cmd = "test"
       expected = ["TEST PASSED"]
       ret = pytest.product.sendCommand(cmd, expected, timeout=15)
       assert ret == 0

**Decorators:**

- ``@pytest.mark.cmd_check("symbol_name")``: Verify ELF symbol exists
- ``@pytest.mark.dep_config("CONFIG_X", "CONFIG_Y")``: Skip if configs not enabled

Parametrized Command Test
--------------------------

Run multiple test variations:

.. code-block:: python

   @pytest.mark.cmd_check("cmocka")
   @pytest.mark.dep_config("CONFIG_TESTS_TESTSUITES", "CONFIG_CM_SYSCALL_TEST")
   @pytest.mark.parametrize("case,expected", [
       ("test1", ["PASSED"]),
       ("test2", ["PASSED"]),
       ("test3", ["OK"])
   ])
   def test_cmocka_cases(case, expected):
       cmd = f"cmocka -t {case}"
       ret = pytest.product.sendCommand(cmd, expected, timeout=300)
       assert ret == 0

Dynamic Test Generation
------------------------

Generate tests from ELF symbols (e.g., LTP tests):

.. code-block:: python

   import pytest
   from ntfc.lib.elf.elf_parser import ElfParser

   def pytest_generate_tests(metafunc):
       if "ltp_case" in metafunc.fixturenames:
           elf = ElfParser("path/to/nuttx")
           cases = elf.get_symbols("ltp_.*_main")
           metafunc.parametrize("ltp_case", cases)

   def test_ltp(ltp_case):
       ret = pytest.product.sendCommand(ltp_case, [], timeout=60)
       assert ret == 0

Available Fixtures and Marks
=============================

NTFC provides built-in fixtures and pytest marks for test development.

**Built-in Fixtures:**

TODO

**Custom Fixtures:**

Define setup/teardown fixtures for test preparation:

.. code-block:: python

   @pytest.fixture(scope="function")
   def setup_device():
       """Setup device state before test."""
       logging.info("Setting up device")
       pytest.product.sendCommand("init_cmd", timeout=2)

       yield  # Test runs here

       # Cleanup
       logging.info("Cleaning up device")
       pytest.product.sendCommand("cleanup_cmd", timeout=2)

   def test_with_setup(setup_device):
       ret = pytest.product.sendCommand("test", ["PASS"], timeout=15)
       assert ret == 0

**Available Marks:**

.. list-table::
   :header-rows: 1

   * - Mark
     - Purpose
     - Example
   * - ``@pytest.mark.cmd_check()``
     - Verify ELF symbol exists before running test
     - ``@pytest.mark.cmd_check("test_main")``
   * - ``@pytest.mark.dep_config()``
     - Skip test if config options not enabled
     - ``@pytest.mark.dep_config("CONFIG_X", "CONFIG_Y")``
   * - ``@pytest.mark.parametrize()``
     - Run test with multiple parameter sets
     - ``@pytest.mark.parametrize("param", [val1, val2])``
   * - ``@pytest.mark.repeat()``
     - Repeat test multiple times
     - ``@pytest.mark.repeat(5)``
   * - ``@pytest.mark.run()``
     - Mark specific tests for execution
     - ``@pytest.mark.run()``
   * - ``@pytest.mark.skip()``
     - Skip test conditionally
     - ``@pytest.mark.skip(reason="not ready")``

**Example - Test Repetition:**

.. code-block:: python

   @pytest.mark.repeat(3)
   def test_stability():
       """Run this test 3 times to check stability."""
       ret = pytest.product.sendCommand("test", ["PASS"], timeout=15)
       assert ret == 0

Product and Command Methods
===========================

``pytest.product`` provides methods to interact with the device:

.. list-table::
   :header-rows: 1

   * - Method
     - Description
     - Example
   * - ``sendCommand(cmd, expected, timeout)``
     - Send command and wait for expected response
     - ``pytest.product.sendCommand("ls", ["root"], timeout=15)``
   * - ``sendCommandReadUntilPattern(cmd, pattern, args, timeout)``
     - Send command to device and read until a specific pattern
     - ``pytest.product.sendCommandReadUntilPattern("hello", ["Hello"], timeout=15)``
