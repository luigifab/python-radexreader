%global common_summary_en Reader for the RADEX RD1212 and ONE Geiger counters
%global common_summary_fr Lecteur pour les compteurs Geiger RADEX RD1212 et ONE

%global common_description_en %{expand:
The RadexReader is an user-space driver for the RADEX RD1212 and
the RADEX ONE Geiger counters. It allow to read and clear stored
data via USB.

To avoid Access denied (insufficient permissions), don't forget
to unplug the device after installation.}

%global common_description_fr %{expand:
Le RadexReader est un pilote en espace utilisateur pour les compteurs
Geiger RADEX RD1212 et RADEX ONE. Il permet de lire et d'effacer les
données stockées via USB.

Pour éviter un Access denied (insufficient permissions), n'oubliez pas
de débrancher l'appareil après l'installation.}

Name:          python-radexreader
Version:       1.2.5
Release:       1%{?dist}
Summary:       %{common_summary_en}
Summary(fr):   %{common_summary_fr}
License:       GPL-2.0-or-later
URL:           https://github.com/luigifab/python-radexreader
Source0:       %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:     noarch
BuildRequires: aspell-fr

%description %{common_description_en}
%description -l fr %{common_description_fr}


%package -n python3-radexreader
%py_provides python3-radexreader
Summary:       %{common_summary_en}
Summary(fr):   %{common_summary_fr}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
Requires:      python3
Requires:      %{py3_dist pyserial}
Requires:      %{py3_dist pyusb}

%description -n python3-radexreader %{common_description_en}
%description -n python3-radexreader -l fr %{common_description_fr}


%prep
%setup -q -n python-radexreader-%{version}
sed -i 's/radexreader-local /python3-radexreader-rpm /g' src/radexreader-cli.py
sed -i 's/\#\!\/usr\/bin\/python3/\#/g' src/radexreader/__init__.py

%build
cd src
%py3_build

%install
cd src
%py3_install
install -Dpm 755 radexreader-cli.py %{buildroot}%{_bindir}/radexreader
install -Dpm 644 ../data/radexreader.1 %{buildroot}%{_mandir}/man1/radexreader.1
install -Dpm 644 ../data/radexreader.fr.1 %{buildroot}%{_mandir}/fr/man1/radexreader.1
install -Dpm 644 ../scripts/debian/python3-radexreader.udev %{buildroot}/lib/udev/rules.d/60-%{name}.rules

%files -n python3-radexreader
%license LICENSE
%doc README.md
%ghost %{python3_sitelib}/radexreader*egg-info/
%{python3_sitelib}/radexreader/
%{_bindir}/radexreader
%{_mandir}/man1/radexreader.1*
%{_mandir}/*/man1/radexreader.1*
/lib/udev/rules.d/60-%{name}.rules


%changelog
* Mon Mar 03 2025 Fabrice Creuzot <code@luigifab.fr> - 1.2.5-1
- New upstream release

* Fri Feb 02 2024 Fabrice Creuzot <code@luigifab.fr> - 1.2.4-1
- New upstream release

* Tue Oct 10 2023 Fabrice Creuzot <code@luigifab.fr> - 1.2.3-1
- New upstream release

* Fri Jun 16 2023 Fabrice Creuzot <code@luigifab.fr> - 1.2.2-2
- Package spec update

* Tue Jun 06 2023 Fabrice Creuzot <code@luigifab.fr> - 1.2.2-1
- New upstream release

* Thu Sep 09 2021 Fabrice Creuzot <code@luigifab.fr> - 1.2.1-1
- New upstream release

* Wed May 05 2021 Fabrice Creuzot <code@luigifab.fr> - 1.2.0-1
- Initial Fedora package release (Closes: rhbz#1896742)
