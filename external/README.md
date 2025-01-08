This directory is intentionally empty.

By default, NTF uses this directory to search for test cases and configuration 
files, which is handy when we use NTF directly from the sources.

The default organization under this directory is as follows:

- ``external/nuttx-testing`` – for test cases

- ``external/ignore.txt`` – for a list of blacklisted test cases

- ``external/config.yaml`` – for the YAML configuration file

- ``external/nuttx`` – for the NuttX kernel source code

- ``external/nuttx-apps`` – for the NuttX apps source code

Each default path can be overridden from the command line with the appropriate 
option.
