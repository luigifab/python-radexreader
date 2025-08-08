#!/bin/bash
# Debian: sudo apt install dpkg-dev devscripts dh-make dh-python dh-exec


cd "$(dirname "$0")"
version="1.3.0"


mkdir builder
rm -rf builder/*

# copy to a tmp directory
if [ true ]; then
	cd builder
	wget https://github.com/luigifab/python-radexreader/archive/v$version/python-radexreader-$version.tar.gz
	tar xzf python-radexreader-$version.tar.gz
	cd ..
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
fi


# create packages for Debian and Ubuntu and MX Linux
for serie in experimental questing plucky oracular noble jammy focal bionic xenial trusty mx23 mx21; do

	printf "\n\n#################################################################### $serie ##\n\n"
	if [ $serie = "experimental" ]; then
		# copy for Ubuntu
		cp -a builder/python-radexreader-$version/ builder/python-radexreader-$version+src/
		cd builder/python-radexreader-$version/
	elif [ $serie = "unstable" ]; then
		rm -rf builder/python-radexreader-$version/
		cp -a builder/python-radexreader-$version+src/ builder/python-radexreader-$version/
		cd builder/python-radexreader-$version/
	else
		cp -a builder/python-radexreader-$version+src/ builder/python-radexreader-$serie-$version/
		cd builder/python-radexreader-$serie-$version/
	fi

	dh_make -s -y -f ../python-radexreader-$version.tar.gz -p python-radexreader

	rm -rf debian/*/*ex debian/*ex debian/*EX debian/README* debian/*doc*
	cp scripts/debian/* debian/
	rm -f debian/deb.sh
	mkdir debian/upstream ; mv debian/metadata debian/upstream/metadata
	chmod +x debian/radexreader*install


	if [ $serie = "experimental" ]; then
		mv debian/control.debian debian/control
		mv debian/changelog.debian debian/changelog
		rm -f debian/*.mx debian/*.debian debian/*.ubuntu
		echo "=========================== buildpackage ($serie) =="
		dpkg-buildpackage -us -uc
	else
		# debhelper: experimental:13 focal/mx19/mx21:12 bionic:9 xenial:9 trusty:9
		if [ $serie = "unstable" ]; then
			mv debian/control.debian debian/control

		elif [ $serie = "mx19" ] || [ $serie = "mx21" ]; then
			mv debian/control.mx debian/control
			sed -i 's/debhelper-compat (= 13)/debhelper-compat (= 12)/g' debian/control
		elif [ $serie = "focal" ]; then
			mv debian/control.ubuntu debian/control
			sed -i 's/debhelper-compat (= 13)/debhelper-compat (= 12)/g' debian/control
		elif [ $serie = "bionic" ]; then
			mv debian/control.ubuntu debian/control
			sed -i 's/execute_before_dh_install:/override_dh_update_autotools_config:/g' debian/rules
			sed -i 's/debhelper-compat (= 13)/debhelper-compat (= 9)/g' debian/control
		elif [ $serie = "xenial" ]; then
			mv debian/control.ubuntu debian/control
			sed -i 's/execute_before_dh_install:/override_dh_update_autotools_config:/g' debian/rules
			sed -i 's/debhelper-compat (= 13)/debhelper (>= 9)/g' debian/control
			sed -i ':a;N;$!ba;s/Rules-Requires-Root: no\n//g' debian/control
			echo 9 > debian/compat
		elif [ $serie = "trusty" ]; then
			mv debian/control.ubuntu debian/control
			sed -i 's/execute_before_dh_install:/override_dh_update_autotools_config:/g' debian/rules
			sed -i 's/debhelper-compat (= 13)/debhelper (>= 9)/g' debian/control
			sed -i ':a;N;$!ba;s/Rules-Requires-Root: no\n//g' debian/control
			echo 9 > debian/compat
		else
			mv debian/control.ubuntu debian/control
		fi
		if [ $serie = "mx23" ] || [ $serie = "mx21" ] || [ $serie = "mx19" ]; then
			mv debian/changelog.mx debian/changelog
			sed -i 's/-1) /-1~'$serie'+1) /' debian/changelog
		elif [ $serie = "unstable" ]; then
			mv debian/changelog.debian debian/changelog
		else
			mv debian/changelog.ubuntu debian/changelog
			sed -i 's/experimental/'$serie'/g' debian/changelog
			sed -i 's/-1) /-1+'$serie') /' debian/changelog
		fi
		rm -f debian/*.mx debian/*.debian debian/*.ubuntu
		echo "=========================== buildpackage ($serie) =="
		dpkg-buildpackage -us -uc -ui -d -S
	fi
	cd ..

	if [ $serie = "experimental" ]; then
		echo "=========================== lintian ($serie) =="
		lintian -EviIL +pedantic python-radexreader_$version*.changes
		rm *amd64.changes
	elif [ $serie = "unstable" ]; then
		echo "=========================== debsign ($serie) =="
		debsign python-radexreader*$version-*_source.changes
	else
		echo "=========================== debsign ($serie) =="
		debsign python-radexreader*$version*$serie*source.changes
	fi
	cd ..
done


printf "\n\n"
ls -dlth "$PWD/"builder/*.deb "$PWD/"builder/*.changes
printf "\n"
rm -rf builder/*/