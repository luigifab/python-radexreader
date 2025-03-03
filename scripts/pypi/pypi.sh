#!/bin/bash
# Debian: sudo apt install python3-pip python3-setuptools
# Fedora: sudo dnf install python3-devel

cd "$(dirname "$0")"
version="1.2.5"
rm -rf builder/

mkdir builder
mkdir builder/radexreader-${version}

# copy to a tmp directory
cp -r ../../src/*  builder/radexreader-${version}/
cp ../../README.md builder/radexreader-${version}/
cp /usr/share/common-licenses/GPL*2                         builder/radexreader-${version}/LICENSE
mv builder/radexreader-${version}/radexreader-cli.py        builder/radexreader-${version}/radexreader/radexreader-cli.py
sed -i 's/radexreader-local /python3-radexreader-pypi /g'   builder/radexreader-${version}/radexreader/radexreader-cli.py
sed -i 's/Usage: radexreader /Usage: radexreader-cli.py /g' builder/radexreader-${version}/radexreader/radexreader-cli.py

# create package (https://packaging.python.org/tutorials/packaging-projects/)
cd builder/radexreader-${version}/
python3 -m pip install --user --upgrade setuptools wheel --no-warn-script-location
python3 setup.py sdist bdist_wheel
cd ../..
mv builder/radexreader-${version}/dist/* .
echo "==========================="
ls -dlth $PWD/*.gz $PWD/*.whl
echo "==========================="

# cleanup
rm -r builder/