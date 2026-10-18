#!/bin/bash
# Fedora: sudo dnf install rpmdevtools rpm-sign python3-devel desktop-file-utils aspell-fr enchant2-aspell
# Fedora: configure: error: C compiler cannot create executables? remove and reinstall glibc-devel gcc

cd "$(dirname "$0")" || exit 1
version="1.4.0"


mkdir -p builder ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
find builder/* ! -name "*$version*.rpm" ! -name "*$version*.gz" -exec rm -rf {} + 2>/dev/null
rm -f ~/rpmbuild/SOURCES/python-radexreader-$version.tar.gz

# copy to a tmp directory
if [ true ]; then
	rm python-radexreader.spec
	wget https://raw.githubusercontent.com/luigifab/python-radexreader/refs/tags/v$version/scripts/fedora/python-radexreader.spec
	chmod 644 python-radexreader.spec
	spectool -g -R python-radexreader.spec
else
	temp=python-radexreader-$version
	mkdir /tmp/$temp
	cp -r ../../* /tmp/$temp/
	rm -rf /tmp/$temp/scripts/*/builder/ /tmp/$temp/src/__pycache__/ /tmp/$temp/src/radexreader/__pycache__/

	mv /tmp/$temp builder/
	cp /usr/share/common-licenses/GPL*2 builder/$temp/LICENSE

	cd builder/
	tar czf $temp.tar.gz $temp
	cd ..

	cp builder/$temp.tar.gz ~/rpmbuild/SOURCES/python-radexreader-$version.tar.gz
	chmod 644 python-radexreader.spec
fi

# create package (rpm sign https://access.redhat.com/articles/3359321)
rpmbuild --quiet -ba python-radexreader.spec
echo "=================================== rpm-sign =="
rpm --addsign ~/rpmbuild/RPMS/*/python*radexreader*.rpm
rpm --addsign ~/rpmbuild/SRPMS/python*radexreader*.rpm
mv ~/rpmbuild/RPMS/*/python*radexreader*.rpm builder/
mv ~/rpmbuild/SRPMS/python*radexreader*.rpm builder/
rpm --checksig builder/*.rpm
echo "=================================== rpm-lint =="
rpmlint python-radexreader.spec builder/*.rpm | grep radexreader
echo "==============================================="
ls -dlth "$PWD"/builder/*.rpm

# cleanup
rm -rf builder/*/