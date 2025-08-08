#!/bin/bash



cd "$(dirname "$0")"
version="1.3.0"


mkdir -p builder builder/{BUILD,RPMS,SRPMS}
find builder/* ! -name "*$version*.rpm" ! -name "*$version*.gz" -exec rm -rf {} + 2>/dev/null


# copy to a tmp directory
if [ true ]; then
	rm python-radexreader.spec
	wget https://raw.githubusercontent.com/luigifab/python-radexreader/refs/tags/v$version/scripts/openmandriva/python-radexreader.spec
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

	cp builder/$temp.tar.gz python-radexreader-$version.tar.gz
	chmod 644 python-radexreader.spec
fi

# create package (rpm sign https://access.redhat.com/articles/3359321)
cp -a python-radexreader-$version.tar.gz python-radexreader.spec builder/
cd builder/
abb builda
rpm --addsign RPMS/*/python*radexreader*.rpm
rpm --addsign SRPMS/python*radexreader*.rpm
mv RPMS/*/python*radexreader*.rpm .
mv SRPMS/python*radexreader*.rpm .
echo "==========================="
rpm --checksig *.rpm
echo "==========================="
rpmlint python-radexreader.spec *.rpm
echo "==========================="
ls -dlth "$PWD/"*.rpm
echo "==========================="
cd ..

# cleanup
rm -rf builder/*/ builder/*buildlog builder/*spec python-radexreader-$version.tar.gz