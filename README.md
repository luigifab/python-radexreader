# RadexReader

The RadexReader is an user-space driver for the [RADEX RD1212 v1/v2](https://quartarad.com/product-category/radiation-detector/) and the [RADEX ONE](https://quartarad.com/product-category/radiation-detector/) Geiger counters. It allow to read and clear stored data via USB. Warning! This tool is completely unrelated with QuartaRad.

This tool was initially developed with RD1212 v2.48.

![RADEX RD1212](images/RD1212.jpg?raw=true)
![RADEX ONE](images/ONE.jpg?raw=true)

## Screenshots and Usage

[![Screnshot 1](images/thumbs/read.png?raw=true)](images/read.png?raw=true)
[![Screnshot 2](images/thumbs/compare.png?raw=true)](images/compare.png?raw=true)

* Read `src/radexreader.py` for examples.
* Run the command `radexreader` available with DEB/RPM packages.
* Run the command `.../radexreader.py` available with PYPI package.

## Installation

It require *libusb*, *pyusb* and *pyserial*.

#### Installation for Debian and Ubuntu

* `sudo apt install python3-radexreader radexreader`

#### Installation for Fedora

* `sudo dnf install python3-radexreader`

#### Installation for openSUSE

* `sudo zypper install python3-radexreader`

#### Installation with PIP

* With Linux: `sudo python3 -m pip install radexreader` (+libusb)
* With Mac: `sudo pip install radexreader` (+libusb)
* With Windows: `python -m pip install radexreader` (+[libusb](https://libusb.info/), put libusb-1.0.dll in system32)

#### Installation with Docker

* `sudo docker run --rm --user root -it --privileged -v /dev:/dev python:3.x-alpine /bin/sh` then: `apk update ; apk add libusb ; python3 -m pip install radexreader`

#### Repository for Debian and Ubuntu

```bash
# PPA: https://launchpad.net/~luigifab/+archive/ubuntu/packages
# with Debian 12+ you can use mantic+ instead of focal (https://unix.stackexchange.com/a/669008/364800)
sudo add-apt-repository ppa:luigifab/packages
sudo apt update
sudo apt install python3-radexreader radexreader
# or
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys FFE5BD439356DF7D
echo "deb http://ppa.launchpad.net/luigifab/packages/ubuntu focal main" | sudo tee -a /etc/apt/sources.list
sudo apt update
sudo apt install python3-radexreader radexreader
# or
sudo wget -O /etc/apt/trusted.gpg.d/luigifab.gpg https://www.luigifab.fr/apt.gpg
echo "deb http://ppa.launchpad.net/luigifab/packages/ubuntu focal main" | sudo tee -a /etc/apt/sources.list
sudo apt update
sudo apt install python3-radexreader radexreader
```
```bash
# sha256sum /etc/apt/trusted.gpg.d/luigifab.gpg
578c89a677048e38007462d543686b53587efba9f93814601169253c45ff9213
# apt-key list
/etc/apt/trusted.gpg.d/luigifab.gpg
pub   rsa4096 2020-10-31 [SC]
      458B 0C46 D024 FD8C B8BC  99CD FFE5 BD43 9356 DF7D
```

## Copyright

- Current version: 1.2.3 (10/10/2023)
- Compatibility: Python 3.3 / 3.4 / 3.5 / 3.6 / 3.7 / 3.8 / 3.9 / 3.10 / 3.11 / 3.12
- Links: [luigifab.fr](https://www.luigifab.fr/python/radexreader) - [github.com](https://github.com/luigifab/python-radexreader) - [pypi.org](https://pypi.org/project/radexreader/)\
[Debian python-radexreader.deb](https://packages.debian.org/python3-radexreader)\
[Fedora python-radexreader.rpm](https://src.fedoraproject.org/rpms/python-radexreader)\
[openSUSE python-radexreader.rpm](https://software.opensuse.org/package/python-radexreader)\
[Ubuntu PPA](https://launchpad.net/~luigifab/+archive/ubuntu/packages)

This program is provided under the terms of the **GNU GPLv2+** license.\
If you like, take some of your time to improve some translations, go to https://bit.ly/2HyCCEc.
