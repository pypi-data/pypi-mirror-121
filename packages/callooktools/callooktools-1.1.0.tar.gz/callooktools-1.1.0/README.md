# callooktools

# **WARNING:** This library is now deprecated. Use [callsignlookuptools](https://pypi.org/project/callsignlookuptools/) instead.

[Callook.info](https://callook.info) API interface in Python

[![PyPI](https://img.shields.io/pypi/v/callooktools)](https://pypi.org/project/callooktools/) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/callooktools) ![PyPI - License](https://img.shields.io/pypi/l/callooktools) [![Documentation Status](https://readthedocs.org/projects/callooktools/badge/?version=latest)](https://callooktools.readthedocs.io/en/latest/?badge=latest)

## Installation

`callooktools` requires Python 3.8 at minimum.

```sh
# synchronous requests only
$ pip install callooktools

# asynchronous aiohttp only
$ pip install callooktools[async]

# both sync and async
$ pip install callooktools[all]

# enable the CLI
$ pip install callooktools[cli]
```

**Note:** If `requests`, `aiohttp`, or `rich` are installed another way, you will also have access to the sync, async, or command-line interface, respectively.

## Documentation

Documentation is available on [ReadTheDocs](https://callooktools.miaow.io/).

## Copyright

Copyright 2021 classabbyamp, 0x5c  
Released under the BSD 3-Clause License.  
See [`LICENSE`](LICENSE) for the full license text.
