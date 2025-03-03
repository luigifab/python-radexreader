#!/bin/bash
# Fedora: sudo dnf install rpmdevtools rpm-sign python3-devel aspell-fr enchant2-aspell
# Fedora: configure: error: C compiler cannot create executables? remove and reinstall glibc-devel gcc

cd "$(dirname "$0")"
version="1.2.5"


mkdir -p builder ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
find builder/* ! -name "*$version*.rpm" ! -name "*$version*.gz" -exec rm -rf {} + 2>/dev/null

# copy to a tmp directory
if [ true ]; then
	chmod 644 python-radexreader.spec
	spectool -g -R python-radexreader.spec
else
	temp=python-radexreader-$version
	mkdir /tmp/$temp
	cp -r ../../* /tmp/$temp/
	rm -rf /tmp/$temp/scripts/*/builder/ /tmp/$temp/radexreader/__pycache__/

	mv /tmp/$temp builder/
	cp /usr/share/common-licenses/GPL*2 builder/$temp/LICENSE

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