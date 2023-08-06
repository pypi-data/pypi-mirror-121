# PPF - Python Package Finder Library

This project is home to a command line interface used
to search PyPi for various projects.

Using this CLI is really simple, just type "pypi" and then
the name of your project.

```sh
pypi <project>
```

The command will be processed and will return the following fields:

* Name
* Version
* Description
* Author
* License
* Python Requirements
* Project URL
* Project URLs
* Classifiers

If the project doesn't qualify or provide for one of these fields,
they will be omitted. License names are only shown if they are under 100 characters,
as some maintainers like to include the LICENSE file content in the field, when
theoretically it should be just the license name. This limit is imposed to take better
care over the UI and aligned representation of data.

### Example Usage

```
pypi pathlib

>>>

pathlib | 1.0.1
~~~~~~~~~~~~~~~
Object-oriented filesystem paths

Author: Antoine Pitrou
License: MIT License
Project URL: https://pypi.org/project/pathlib/

Project URLs:
- Download: https://pypi.python.org/pypi/pathlib/
- Homepage: https://pathlib.readthedocs.org/

Classifiers:
- Topic :: Software Development :: Libraries
- Topic :: System :: Filesystems
- License :: OSI Approved :: MIT License
- Operating System :: OS Independent
- Intended Audience :: Developers
- Development Status :: 5 - Production/Stable
- Programming Language :: Python :: 2.6
- Programming Language :: Python :: 2.7
- Programming Language :: Python :: 3
- Programming Language :: Python :: 3.2
- Programming Language :: Python :: 3.3
- Programming Language :: Python :: 3.4
```

### Installation

Install through pip:

```sh
pip install ppfl
```

### Requirements

The ``requests`` module is required for this CLI.
