=========================================
Test Session Configuration (session.json)
=========================================

This file allows you to fine-tune test execution: module inclusion/exclusion
and argument overrides. Path to test session configuration file is passed with
``--jsonconf PATH`` option.

**Structure:**

.. code-block:: json

   {
     "module": {
       "include_module": [
         "Nuttx_System_Arch_Os_Integration",
         "Nuttx_System_Tools"
       ],
       "exclude_module": [
         "Nuttx_System_Arch_Os_Performance"
       ],
       "order": []
     },
     "args": {
       "kv": []
     }
   }

**Fields:**

- **include_module**: Modules to include (empty = include all)
- **exclude_module**: Modules to exclude
- **order**: Force execution order (not supported yet)
- **args.kv**: Configuration overrides (not supported yet)

Module Name Generation
======================

Module names in ``session.json`` combine base module name from ``ntfc.yaml``
with test case directory path.

**Rule:**

1. Start with ``module`` field from ``ntfc.yaml``
2. Append directory path but replace ``/`` with ``_``
3. Capitalize first letter of each directory

**Examples:**

- Base: ``Nuttx_System``, Path: ``arch/os/integration/`` -> ``Nuttx_System_Arch_Os_Integration``
- Base: ``CUSTOM``, Path: ``dir1/dir2/dir3/`` -> ``CUSTOM_Dir1_Dir2_Dir3``

**Usage:**

Include specific modules:

.. code-block:: json

   {
     "module": {
       "include_module": [
         "Nuttx_System_Arch_Os_Integration",
         "Nuttx_System_Tools_Gdb"
       ],
       "exclude_module": []
     }
   }

Exclude specific modules:

.. code-block:: json

   {
     "module": {
       "include_module": [],
       "exclude_module": [
         "Nuttx_System_Arch_Os_Performance"
       ]
     }
   }
