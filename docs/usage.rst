=====
Usage
=====

Commands
========

You can run NTFC as a Python module:

.. code-block:: bash

   python -m ntfc [OPTIONS] COMMAND [ARGS]...

For commands details use ``--help`` option.

``collect`` command
-------------------

Collect-only test cases.

.. code-block:: bash

   python -m ntfc collect [OPTIONS] [COLLECT]


The ``COLLECT`` argument specify what data to print:

* ``collected`` - print collected items only.

* ``skipped`` - print skipped items only.

* ``all``-  (DEFAULT) print all possible data.

* ``silent`` - don't print any additional data.

Options:

* ``--testpath PATH`` - Path to test cases.
  Can be also set with environment variable ``NTFC_TESTPATH``.
  Default: ``./external/nuttx-testing``

* ``--confpath PATH`` - Path to test configuration file.
  Can be also set with environmentvariable ``NTFC_CONFPATH``.
  Default: ``./external/config.yaml``

* ``--ignorefile PATH`` - Path to file with test ignore rules.
  Default: ``./external/ignore.txt``


``test`` command
----------------

Run test cases.

.. code-block:: bash

   python -m ntfc test [OPTIONS]

Options:

* ``--xml`` - Store the XML report.

* ``--resdir PATH`` - Where to store the test results.
  Default: ./result

* ``--testpath PATH`` - Path to test cases.
  Can be also set with environment variable ``NTFC_TESTPATH``.
  Default: ``./external/nuttx-testing``

* ``--confpath PATH`` - Path to test configuration file.
  Can be also set with environmentvariable ``NTFC_CONFPATH``.
  Default: ``./external/config.yaml``

* ``--ignorefile PATH`` - Path to file with test ignore rules.
  Default: ``./external/ignore.txt``

* ``--nologs`` - When set, test logs are not saved locally

``build`` command
----------------

Build NuttX test image from YAML configuration and try to flash.

.. code-block:: bash

   python -m ntfc build [OPTIONS]

Options:

* ``--confpath PATH`` - Path to test configuration file.
  Can be also set with environmentvariable ``NTFC_CONFPATH``.
  Default: ``./external/config.yaml``

* ``--noflash`` - Don't try to flash image to DTU.
