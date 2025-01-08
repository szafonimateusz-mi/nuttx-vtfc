===========
Quick start
===========

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

5. Configure and build NuttX in ``external/nuttx``.

   A sample configuration for ``SIMULATOR`` and ``QEMU-X86_64`` can
   be found at ``docs/boards``.

   For ``SIMULATOR``::

     cd external/nuttx
     mkdir boards/sim/sim/sim/configs/ntfc
     cp ../../docs/boards/sim/defconfig boards/sim/sim/sim/configs/ntfc
     ./tools/configure.sh sim/ntfc
     make -j
     cd ../..

   For ``QEMU-X86_64``::

     mkdir boards/x86_64/intel64/qemu-intel64/configs/ntfc
     cp ../../docs/boards/qemu-intel64/defconfig boards/x86_64/intel64/qemu-intel64/configs/ntfc
     ./tools/configure.sh qemu-intel64/ntfc
     make -j
     cd ../..

6. Collect test cases without running tests.

   For ``SIMULATOR``::

     python -m ntfc --confpath config/nuttx-sim.yaml collect

   For ``QEMU-X86_64``::

     python -m ntfc --confpath config/nuttx-qemu-x86_64.yaml collect

   When you run NTFC with ``--debug`` option, tests that were detected but
   the conditions for running them are not met will also be listed.

7. Run test cases.

   For ``SIMULATOR``::

     python -m ntfc --confpath config/nuttx-sim.yaml test

   For ``QEMU-X86_64``::

     python -m ntfc --confpath config/nuttx-qemu-x86_64.yaml test
