Name:          python-radexreader
Version:       1.3.0
Release:       1
Summary:       Reader for the RADEX RD1212 and ONE Geiger counters
Summary(fr):   Lecteur pour les compteurs Geiger RADEX RD1212 et ONE
License:       GPL-2.0-or-later
Group:         Development/Python
URL:           https://github.com/luigifab/python-radexreader
Source0:       %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:     noarch
BuildRequires: aspell-fr
BuildRequires: python%{pyver}dist(setuptools)
Requires:      pkgconfig(python3)
Requires:      python%{pyver}dist(pyserial)
Requires:      python%{pyver}dist(pyusb)

%description %{expand:
The RadexReader is an user-space driver for the RADEX RD1212 and
the RADEX ONE Geiger counters. It allow to read and clear stored
data via USB.

To avoid Access denied (insufficient permissions), don't forget
to unplug the device after installation.}

%description -l fr %{expand:
Le RadexReader est un pilote en espace utilisateur pour les compteurs
Geiger RADEX RD1212 et RADEX ONE. Il permet de lire et d'effacer les
données stockées via USB.

Pour éviter un Access denied (insufficient permissions), n'oubliez pas
de débrancher l'appareil après l'installation.}


%prep
%setup -q -n python-radexreader-%{version}
sed -i 's/radexreader-local /python-radexreader-rpm /g' src/radexreader-cli.py
sed -i 's/\#\!\/usr\/bin\/python3/\#/g' src/radexreader/__init__.py

%build
cd src
%py3_build

%install
cd src
%py3_install
install -Dpm 755 radexreader-cli.py %{buildroot}%{_bindir}/radexreader
install -Dpm 644 ../data/radexreader.bash %{buildroot}%{_datadir}/bash-completion/completions/radexreader
install -Dpm 644 ../data/radexreader.1 %{buildroot}%{_mandir}/man1/radexreader.1
install -Dpm 644 ../data/radexreader.fr.1 %{buildroot}%{_mandir}/fr/man1/radexreader.1
install -Dpm 644 ../scripts/debian/python3-radexreader.udev %{buildroot}/lib/udev/rules.d/60-%{name}.rules

%files
%license LICENSE
%doc README.md
%ghost %{python3_sitelib}/radexreader*egg-info/
%{python3_sitelib}/radexreader/
%{_bindir}/radexreader
%{_datadir}/bash-completion/completions/radexreader
%{_mandir}/man1/radexreader.1*
%{_mandir}/*/man1/radexreader.1*
/lib/udev/rules.d/60-%{name}.rules


%changelog
* Fri Aug 08 2025 Fabrice Creuzot <code@luigifab.fr> - 1.3.0-1
- New upstream release

* Mon Mar 03 2025 Fabrice Creuzot <code@luigifab.fr> - 1.2.5-1
- Initial OpenMandriva package release (Closes: #3169)


















