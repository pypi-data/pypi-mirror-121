# pdcommandline - library to build multithreaded interactive command line applications

A cross platform library to build multithreaded command line applications with formatted output, command line parsing and context sensitive command line completion.

## ***pdcommandline*** features:
* VT100 support for colored formatting of the output
* colored and styled strings
* table and tree formatting
* logging with filtering for verbosity levels
* thread safe access for multi threaded applications
* worker and background threads
* lifecycle management of threads
* multiline progess display
* customizable interactive keyboard input
* handling of CTRL+C signals with support of hooks
* command line parsing
    * context sensitive help
    * context sensitive command completion

***NOTE***: The current implementation of ***pdcommandline*** is a prototype. It’s assumed that the API will change in future releases.

## Getting started
* Install from [PyPI](https://pypi.org/project/pdcommandline)
* Checkout the [sources](https://gitlab.com/pdbuild/pdcommandline)