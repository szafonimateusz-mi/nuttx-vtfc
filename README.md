# NTFC

NuttX Test Framework for Community.

This tool requires at least Python 3.10. Not tested with earlier versions of Python.

## Features

- NuttX simulator and QEMU devices are supported now
- run the command from NSH and wait for the expected result
- OS crash detection and busy loop detection
- detection of supported test cases for a given NuttX image based on 
the configuration and image ELF file

## Installation

At the moment the package can only be installed from source.
Details on installing from source can be found in [CONTRIBUTING.md](CONTRIBUTING.md).

## Usage

For a quick start quid, see [docs/quickstart](docs/quickstart.rst).

For usage details, look at [docs/usage](docs/usage.rst).

### Preparing the image for testing

NuttX image requirements for tests:

- ``CONFIG_DEBUG_SYMBOLS`` must be set.
- NSH must be enabled and set as entry point
- ``CONFIG_DEBUG_FEATURES=y`` and ``CONFIG_DEBUG_ASSERTIONS=y`` are recommended.

### Test cases

- https://github.com/szafonimateusz-mi/nuttx-testing

## Optiopnal dependencies

- pytest-html - for HTML test reports
- pytest-json - for JSON test reports

## Contributing

To get started with developing NTFC, see [CONTRIBUTING.md](CONTRIBUTING.md).

The list of current TODOs can be found in [TODO.md](TODO.md).
