===========
Quick start
===========

Common initialization
=====================

1. Clone the NTFC repository::

     git clone <PATH_TO_NTFC_REPO>
     cd nuttx-ntfc

2. Create and activate a virtual environment::

     virtualenv venv
     source venv/bin/activate

3. Install the project in editable mode::

     pip install -e .

4. Prepare the test environment::

     git clone https://github.com/apache/nuttx.git external/nuttx
     git clone https://github.com/apache/nuttx-apps.git external/nuttx-apps
     git clone https://github.com/szafonimateusz-mi/nuttx-testing external/nuttx-testing


Prepare NuttX boards
====================

First make sure the configuration is copied to NuttX directory.

For ``SIMULATOR``::

     mkdir external/nuttx/boards/sim/sim/sim/configs/ntfc
     cp docs/boards/sim/defconfig external/nuttx/boards/sim/sim/sim/configs/ntfc

For ``QEMU-X86_64``::

     mkdir external/nuttx/boards/x86_64/intel64/qemu-intel64/configs/ntfc
     cp docs/boards/qemu-intel64/defconfig external/nuttx/boards/x86_64/intel64/qemu-intel64/configs/ntfc

For ``QEMU-ARMV7A``::

     mkdir external/nuttx/boards/arm/qemu/qemu-armv7a/configs/ntfc
     cp docs/boards/qemu-armv7a/defconfig external/nuttx/boards/arm/qemu/qemu-armv7a/configs/ntfc

For ``QEMU-ARMV7R``::

     mkdir external/nuttx/boards/arm/qemu/qemu-armv7r/configs/ntfc
     cp docs/boards/qemu-armv7r/defconfig external/nuttx/boards/arm/qemu/qemu-armv7r/configs/ntfc

For ``QEMU-ARMV8A``::

     mkdir external/nuttx/boards/arm64/qemu/qemu-armv8a/configs/ntfc
     cp docs/boards/qemu-armv8a/defconfig external/nuttx/boards/arm64/qemu/qemu-armv8a/configs/ntfc

For ``QEMU-RISCV64``::

     mkdir boards/risc-v/qemu-rv/rv-virt/configs/ntfc64
     cp docs/boards/qemu-riscv-rv-virt-64/defconfig external/nuttx/boards/risc-v/qemu-rv/rv-virt/configs/ntfc64

For ``NUCLEO-H743ZI``::

     mkdir boards/arm/stm32h7/nucleo-h743zi/configs/ntfc
     cp ../../docs/boards/nucleo-h743zi/defconfig boards/arm/stm32h7/nucleo-h743zi/configs/ntfc

Automatically build DUT images
==============================

The tool allows you to automatically build configurations and run tests on
the created NuttX image.

Then run the ``test`` command that build which will build the image
and start testing.

For ``SIMULATOR``::

     python -m ntfc test --confpath config/nuttx-sim.yaml

For ``QEMU-X86_64``::

     python -m ntfc test --confpath config/nuttx-qemu-x86_64.yaml

For ``QEMU-ARMV7A``::

     python -m ntfc test --confpath config/nuttx-qemu-armv7a.yaml

For ``QEMU-ARMV7R``::

     python -m ntfc test --confpath config/nuttx-qemu-armv7r.yaml

For ``QEMU-ARMV8A``::

     python -m ntfc test --confpath config/nuttx-qemu-armv8a.yaml

For ``QEMU-RISCV64``::

     python -m ntfc test --confpath config/nuttx-qemu-riscv-rv-virt-64.yaml

There is also a configuration available that builds the all available
QEMU and SIM targets and runs parallel tests on all DUTs::

  python -m ntfc test --confpath=./config/nuttx-build-qemu-sim-ntfc.yaml

You can also run ``build`` command that only build image without starting tests.

Automatic build and Flash
=========================

For ``NUCLEO-H743ZI`` there is availalbe configuration that automatically
build, flash and test image ::

1. Build image and flash::

     python -m ntfc build --confpath config/nuttx-nucleo-h743zi.yaml

2. Collect test cases without running tests::

     python -m ntfc collect --confpath config/nuttx-nucleo-h743zi.yaml

3. Run test cases::

     python -m ntfc test --confpath config/nuttx-nucleo-h743zi.yaml

Creating a DUT image manually
=============================

You can always manually build the NuttX image. Currently, such an example
is available in ``config/nuttx-custom-image.yaml``. Commands are the same
like before:

1. Collect test cases without running tests::

     python -m ntfc collect --confpath config/nuttx-custom-image.yaml

2. Run test cases::

     python -m ntfc test --confpath config/nuttx-custom-image.yaml
