#!/bin/bash
# openSUSE: sudo zypper install rpmdevtools rpm-build python3-devel aspell-fr


cd "$(dirname "$0")"
version="1.3.0"


mkdir -p builder ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
find builder/* ! -name "*$version*.rpm" ! -name "*$version*.gz" -exec rm -rf {} + 2>/dev/null
rm -f ~/rpmbuild/SOURCES/python-radexreader-$version.tar.gz

# copy to a tmp directory
if [ true ]; then
	rm python-radexreader.spec
	wget https://raw.githubusercontent.com/luigifab/python-radexreader/refs/tags/v$version/scripts/opensuse/python-radexreader.spec
	chmod 644 python-radexreader.spec
	spectool -g -R python-radexreader.spec
else
	temp=python-radexreader-$version
	mkdir /tmp/$temp
	cp -r ../../* /tmp/$temp/
	rm -rf /tmp/$temp/scripts/*/builder/ /tmp/$temp/radexreader/__pycache__/

	mv /tmp/$temp builder/
	cp /usr/share/licenses/*-firmware/GPL-2 builder/$temp/LICENSE # * = kernel

	cd builder/
	tar czf $temp.tar.gz $temp
	cd ..

	cp builder/$temp.tar.gz ~/rpmbuild/SOURCES/python-radexreader-$version.tar.gz
	chmod 644 python-radexreader.spec
fi

# create package (rpm sign https://access.redhat.com/articles/3359321)
rpmbuild -ba python-radexreader.spec
rpm --addsign ~/rpmbuild/RPMS/*/python*radexreader*.rpm
rpm --addsign ~/rpmbuild/SRPMS/python*radexreader*.rpm
mv ~/rpmbuild/RPMS/*/python*radexreader*.rpm builder/
mv ~/rpmbuild/SRPMS/python*radexreader*.rpm builder/
echo "==========================="
rpm --checksig builder/*.rpm
echo "==========================="
rpmlint python-radexreader.spec builder/*.rpm
echo "==========================="
ls -dlth "$PWD/"builder/*.rpm
echo "==========================="

# cleanup
rm -rf builder/*/