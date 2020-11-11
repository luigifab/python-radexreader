# RadexReader

The RadexReader is an user-space driver for the [RADEX RD1212](https://quartarad.com/product-category/radiation-detector/) Geiger counter. It allow to read and clear stored data via USB. Warning! This tool is completely unrelated with QuartaRad.

Debian and Fedora packages submitted: [deb](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=974217), [rpm](https://bugzilla.redhat.com/show_bug.cgi?id=1896742). Ubuntu: [PPA](https://launchpad.net/~luigifab/+archive/ubuntu/packages).

## Installation

It require *libusb*.

* Debian and Ubuntu: `sudo apt install python3-radexreader radexreader` (coming soon, or via PPA)

* Fedora: `sudo dnf install python3-radexreader` (coming soon)

* Linux: `sudo python3 -m pip install pyusb radexreader` (+libusb)

* Mac: `sudo pip install pyusb radexreader` (+libusb)

* Windows: `python -m pip install pyusb radexreader` (+[libusb](https://libusb.info/), put libusb-1.0.dll in system32)

* Docker Alpine: `sudo docker run --rm --user root -it --privileged -v /dev:/dev python:3.x-alpine /bin/sh` then: `apk update ; apk add libusb ; python3 -m pip install pyusb radexreader`

## Usage and Screenshots

* Read `src/cmd.py` for usage examples.
* Run the command `radexreader` available with DEB/RPM packages.
* Run the command `cmd.py` available with PYPI package.

[![Screnshot 1](images/thumbs/read.png?raw=true)](images/read.png?raw=true)
[![Screnshot 2](images/thumbs/compare.png?raw=true)](images/compare.png?raw=true)

## Copyright

- Current version: 1.0.0 (11/11/2020)
- Compatibility: Python 3.3 / 3.4 / 3.5 / 3.6 / 3.7 / 3.8 / 3.9
- Links: [PYPI package](https://pypi.org/project/radexreader/), [PPA](https://launchpad.net/~luigifab/+archive/ubuntu/packages)

This program is provided under the terms of the *GNU GPLv2+* license.
