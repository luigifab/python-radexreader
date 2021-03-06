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
Version:       1.2.0
Release:       1%{?dist}
Summary:       %{common_summary_en}
Summary(fr):   %{common_summary_fr}
License:       GPLv2+
URL:           https://github.com/luigifab/python-radexreader
Source0:       %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:     noarch
BuildRequires: hunspell-fr

%description %{common_description_en}
%description -l fr %{common_description_fr}


%package -n python3-radexreader
%py_provides python3-radexreader
Summary:       %{common_summary_en}
Summary(fr):   %{common_summary_fr}

BuildRequires: python3-devel
Requires:      python3
Requires:      %{py3_dist pyserial}
Requires:      %{py3_dist pyusb}

%description -n python3-radexreader %{common_description_en}
%description -n python3-radexreader -l fr %{common_description_fr}


%prep
%setup -q -n python-radexreader-%{version}
sed -i 's/python3-radexreader /python3-radexreader-rpm /g' src/radexreader.py
sed -i 's/\#\!\/usr\/bin\/python3/\#/g' src/radexreader/__init__.py

%build
cd src
%py3_build

%install
cd src
%py3_install
mkdir -p %{buildroot}%{_bindir}/
mkdir -p %{buildroot}/lib/udev/rules.d/
install -p -m 644 ../debian/udev %{buildroot}/lib/udev/rules.d/60-python3-radexreader.rules
install -p -m 755 ../src/radexreader.py %{buildroot}%{_bindir}/radexreader

%files -n python3-radexreader
%license LICENSE
%doc README.md
%{_bindir}/radexreader
%{python3_sitelib}/radexreader/
%{python3_sitelib}/radexreader*egg-info/
/lib/udev/rules.d/60-python3-radexreader.rules


%changelog
* Wed May 05 2021 Fabrice Creuzot <code@luigifab.fr> - 1.2.0-1
- Initial fedora package release (Closes: rhbz#1896742)
