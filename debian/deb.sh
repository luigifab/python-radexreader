#!/bin/bash
# debian: sudo apt install dpkg-dev devscripts dh-make dh-python dh-exec



cd "$(dirname "$0")"
version="1.1.0"


rm -rf builder/
mkdir builder

# copy to a tmp directory
if [ true ]; then
	cd builder
	wget https://github.com/luigifab/python-radexreader/archive/v${version}/python-radexreader-${version}.tar.gz
	tar xzf python-radexreader-${version}.tar.gz
	cd ..
else
	temp=python-radexreader-${version}
	mkdir /tmp/${temp}
	cp -r ../* /tmp/${temp}/
	rm -rf /tmp/${temp}/*/builder/ /tmp/${temp}/radexreader/__pycache__/

	mv /tmp/${temp} builder/
	cp /usr/share/common-licenses/GPL-2 builder/${temp}/LICENSE

	cd builder/
	tar czf ${temp}.tar.gz ${temp}
	cd ..
fi


# create packages for debian and ubuntu
for serie in unstable hirsute groovy focal bionic xenial trusty precise; do

	if [ $serie = "unstable" ]; then
		# for ubuntu
		cp -a builder/python-radexreader-${version}/ builder/python-radexreader-${version}+src/
		# debian only
		cd builder/python-radexreader-${version}/
	else
		# ubuntu only
		cp -a builder/python-radexreader-${version}+src/ builder/python-radexreader-${version}+${serie}/
		cd builder/python-radexreader-${version}+${serie}/
	fi

	dh_make -a -s -y -f ../python-radexreader-${version}.tar.gz -p python-radexreader

	rm -f debian/*ex debian/*EX debian/README* debian/*doc*
	mkdir debian/upstream
	mv debian/metadata     debian/upstream/metadata
	mv debian/udev         debian/python3-radexreader.udev
	mv debian/metainfo.xml debian/python3-radexreader.metainfo.xml
	chmod +x debian/radexreader.install

	if [ $serie = "unstable" ]; then
		dpkg-buildpackage -us -uc
	else
		# debhelper: unstable:13 hirsute:13 groovy:13 focal:12 bionic:9 xenial:9 trusty:9 precise:9
		if [ $serie = "focal" ]; then
			sed -i 's/debhelper-compat (= 13)/debhelper-compat (= 12)/g' debian/control
		fi
		if [ $serie = "bionic" ]; then
			sed -i 's/debhelper-compat (= 13)/debhelper-compat (= 9)/g' debian/control
		fi
		if [ $serie = "xenial" ]; then
			sed -i 's/debhelper-compat (= 13)/debhelper (>= 9)/g' debian/control
			sed -i ':a;N;$!ba;s/Rules-Requires-Root: no\n//g' debian/control
			echo 9 > debian/compat
		fi
		if [ $serie = "trusty" ]; then
			sed -i 's/debhelper-compat (= 13)/debhelper (>= 9)/g' debian/control
			sed -i ':a;N;$!ba;s/Rules-Requires-Root: no\n//g' debian/control
			echo 9 > debian/compat
		fi
		if [ $serie = "precise" ]; then
			sed -i 's/debhelper-compat (= 13)/debhelper (>= 9)/g' debian/control
			sed -i ':a;N;$!ba;s/Rules-Requires-Root: no\n//g' debian/control
			sed -i 's/, dh-python//g' debian/control
			echo 9 > debian/compat
		fi
		sed -i 's/unstable/'${serie}'/g' debian/changelog
		sed -i 's/-1) /-1+'${serie}') /' debian/changelog
		dpkg-buildpackage -us -uc -ui -d -S
	fi
	echo "==========================="
	cd ..

	if [ $serie = "unstable" ]; then
		# debian only
		debsign python-radexreader_${version}-*.changes
		echo "==========================="
		lintian -EviIL +pedantic python-radexreader_${version}-*.deb
	else
		# ubuntu only
		debsign python-radexreader_${version}*+${serie}*source.changes
	fi
	echo "==========================="
	cd ..
done

ls -dltrh $PWD/builder/*.deb $PWD/builder/*.changes
echo "==========================="

# cleanup
rm -rf builder/*/