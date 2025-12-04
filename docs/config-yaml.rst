====================================
Products Configuration (config.yaml)
====================================

This file defines device-under-test (DUT) setup and global configuration.

**Structure for single DUT:**

.. code-block:: yaml

   config:
     # global configuration

   product:
     name: "product-name"     # Product identifier
     cores:                   # List of product cores
       core0:                 # Core0 entry
         name: 'core0-name'
         device: 'sim|qemu|serial'
         # Device-specific configuration

       core1:                 # Core1 entry
         name: 'core1-name'
         device: 'sim|qemu|serial'
         # Device-specific configuration


**Structure for many DUT:**

.. code-block:: yaml

   config:
     # global configuration

   product0:
     name: "product0-name"    # Product 0 identifier
     cores:
       core0:
         name: 'core-name'
         device: 'sim|qemu|serial'
         # Device-specific configuration

   product1:
     name: "product1-name"    # Product 1 identifier
     cores:
       core0:
         name: 'core-name'
         device: 'sim|qemu|serial'
         # Device-specific configuration


The file structure is prepared to support multi-core test cases,
but this is not yet supported in NTFC.

Device Types
============

Simulator (sim)
---------------

.. code-block:: yaml

   cores:
     core0:
       name: 'main'
       device: 'sim'
       exec_path: ''   # empty for sim
       exec_args: ''   # empty for sim

QEMU
----

.. code-block:: yaml

   cores:
     core0:
       name: 'main'
       device: 'qemu'
       exec_path: 'qemu-system-arm'
       exec_args: '-cpu cortex-a7 -nographic -machine virt'

Common QEMU executables: ``qemu-system-arm``, ``qemu-system-aarch64``,
``qemu-system-i386``, ``qemu-system-x86_64``, ``qemu-system-riscv64``

Serial Device
-------------

For real hardware with UART communication:

.. code-block:: yaml

   cores:
     core0:
       name: 'main'
       device: 'serial'
       exec_path: '/dev/ttyACM0'
       exec_args: '115200,n,8,1'
       defconfig: 'boards/arm/stm32h7/nucleo-h743zi/configs/ntfc'
       flash: 'st-flash write $IMAGE_BIN 0x08000000'
       reboot: 'st-flash reset'

**Serial Settings Format:** ``BAUDRATE,PARITY,DATABITS,STOPBITS``

- BAUDRATE: 9600, 19200, 38400, 57600, 115200, etc.
- PARITY: 'n' (None), 'e' (Even), 'o' (Odd), 'm' (Mark), 's' (Space)
- DATABITS: 5, 6, 7, or 8
- STOPBITS: 1, 1.5, or 2

Configuration Approaches
========================

**Auto-build:**

NTFC can automatically builds NuttX with CMake when core configuration has:

.. code-block:: yaml

   defconfig: 'path/to/nuttx/defconfig'

Build directory and path to NuttX repositories must be specified in global
configuration section:

.. code-block:: yaml

  config:
    cwd: './external'
    build_dir: './build'     # Build output directory

Use when:

- Fresh build needed for each test run
- Development/testing workflow
- Easier to use

**Pre-compiled ELF:**

Use existing NuttX binary and skip build step when product configuration has:

.. code-block:: yaml

   elf_path: './external/nuttx/nuttx'
   conf_path: './external/nuttx/.config'

Use when:

- Faster repeated test runs
- Pre-built test images available
- CI environments with cached binaries

**Flash and Reboot (real hardware):**

Automate firmware deployment and device reset is handled with two parameters:

- ``flash``: System command executed before tests
- ``reboot``: System command to reset device between test runs

Flash command can use special tags that are handled by NTFC:

- ``$IMAGE_BIN`` is replaced by path to ``nuttx.bin``.
- ``$IMAGE_HEX`` is replaced by path to ``nuttx.hex``.

Example usage with ``st-flash`` tool:

.. code-block:: yaml

   flash: 'st-flash write $IMAGE_BIN 0x08000000'
   reboot: 'st-flash reset'

Core Configuration Fields
=========================

.. list-table::
   :header-rows: 1

   * - Field
     - Description
   * - ``name``
     - Human-readable core name
   * - ``device``
     - Device type: ``sim``, ``qemu``, or ``serial``
   * - ``exec_path``
     - QEMU executable name or serial port device (``/dev/ttyACM0``, ``COM1``,
       etc.)
   * - ``exec_args``
     - QEMU arguments or serial settings
   * - ``defconfig``
     - Path to NuttX defconfig (auto-build)
   * - ``elf_path``
     - Path to ELF binary (pre-compiled)
   * - ``conf_path``
     - Path to NuttX ``.config`` file (pre-compiled)
   * - ``flash``
     - System command to flash firmware (work in progress)
   * - ``reboot``
     - System command to reboot device
