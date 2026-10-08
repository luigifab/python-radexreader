#!/bin/bash
# Debian: sudo apt install dpkg-dev devscripts dh-make dh-python dh-exec


cd "$(dirname "$0")" || exit 1
export DH_QUIET=1
version="1.4.0"


mkdir -p builder
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
	rm -rf /tmp/$temp/scripts/*/builder/ /tmp/$temp/src/radexreader/__pycache__/

	mv /tmp/$temp builder/
	cp /usr/share/common-licenses/GPL*2 builder/$temp/LICENSE

	cd builder/
	tar czf $temp.tar.gz $temp
	cd ..
fi


# build binary packages for Debian and source packages for Ubuntu and MX Linux
for serie in experimental stonking resolute noble jammy focal bionic xenial trusty mx25 mx23; do

	printf "\n\n#################################################################### $serie\n\n"
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
	rm -f debian/*.sh
	mkdir debian/upstream ; mv debian/metadata debian/upstream/metadata
	chmod +x debian/radexreader*install


	# debhelper: experimental:14 ubuntu:13 focal:12 bionic:9 xenial:9 trusty:9
	if [ $serie = "experimental" ] || [ $serie = "unstable" ]; then
		mv debian/control.debian debian/control
	elif [ $serie = "focal" ]; then
		mv debian/control.ubuntu debian/control
		sed -i 's/debhelper-compat (= 14)/debhelper-compat (= 12)/g' debian/control
	elif [ $serie = "bionic" ]; then
		mv debian/control.ubuntu debian/control

		sed -i 's/execute_before_dh_install:/override_dh_update_autotools_config:/g' debian/rules
		sed -i 's/debhelper-compat (= 14)/debhelper-compat (= 9)/g' debian/control
	elif [ $serie = "xenial" ]; then
		mv debian/control.ubuntu debian/control

		sed -i 's/execute_before_dh_install:/override_dh_update_autotools_config:/g' debian/rules
		sed -i 's/debhelper-compat (= 14)/debhelper (>= 9)/g' debian/control
		sed -i ':a;N;$!ba;s/Rules-Requires-Root: no\n//g' debian/control
		echo 9 > debian/compat
	elif [ $serie = "trusty" ]; then
		mv debian/control.ubuntu debian/control
		sed -i 's/dh $@/dh $@ --with autotools_dev/g' debian/rules
		sed -i 's/execute_before_dh_install:/override_dh_autotools-dev_updateconfig:/g' debian/rules
		sed -i 's/debhelper-compat (= 14)/debhelper (>= 9), autotools-dev/g' debian/control
		sed -i ':a;N;$!ba;s/Rules-Requires-Root: no\n//g' debian/control
		echo 9 > debian/compat
	else
		mv debian/control.ubuntu debian/control
		sed -i 's/debhelper-compat (= 14)/debhelper-compat (= 13)/g' debian/control
	fi

	if [ $serie = "mx25" ] || [ $serie = "mx23" ]; then
		mv debian/changelog.mx debian/changelog
		sed -i 's/-1) /-1~'$serie'+1) /' debian/changelog
		sed -i 's/ experimental; / mx; /' debian/changelog
		sed -i 's/ unstable; / mx; /' debian/changelog
	elif [ $serie = "experimental" ] || [ $serie = "unstable" ]; then
		sed -i 's/ experimental; / '$serie'; /g' debian/changelog
		mv debian/changelog.debian debian/changelog
	else
		sed -i 's/ experimental; / '$serie'; /g' debian/changelog
		sed -i 's/-1) /-1+'$serie') /' debian/changelog
	fi
	rm -f debian/*.mx debian/*.debian debian/*.ubuntu

	if [ $serie = "experimental" ]; then
		echo "===================== build package ($serie) =="
		dpkg-buildpackage -us -uc
		echo "=========================== lintian ($serie) =="
		lintian -EviIL +pedantic ../python-radexreader_$version*.changes
		rm ../*amd64.changes
	fi

	echo "============== build source package ($serie) =="
	rm -f debian/*.sh
	dpkg-buildpackage -us -uc -ui -d -S
	cd ..

	if [ $serie = "experimental" ] || [ $serie = "unstable" ]; then
		echo "=========================== debsign ($serie) =="
		debsign python-radexreader*$version-*_source.changes
	else
		echo "=========================== debsign ($serie) =="
		debsign python-radexreader*$version*$serie*source.changes
	fi
	cd ..
done


printf "\n\n"
ls -dlth "$PWD"/builder/*.deb "$PWD"/builder/*.changes
printf "\n"
rm -rf builder/*/