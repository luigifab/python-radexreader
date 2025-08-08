Name:          python-radexreader
Version:       1.3.0
Release:       0
Summary:       Reader for the RADEX RD1212 and ONE Geiger counters
License:       GPL-2.0-or-later
URL:           https://github.com/luigifab/python-radexreader
Source0:       %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:     noarch
BuildRequires: %{python_module pip}
BuildRequires: %{python_module pyserial}
BuildRequires: %{python_module pyusb}
BuildRequires: %{python_module setuptools}
BuildRequires: %{python_module wheel}
BuildRequires: aspell-fr
BuildRequires: fdupes
BuildRequires: python-rpm-macros
Requires:      python-pyserial
Requires:      python-pyusb
Requires(post):   update-alternatives
Requires(postun): update-alternatives
%python_subpackages

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
sed -i 's/radexreader-local /python3-radexreader-rpm /g' src/radexreader-cli.py
sed -i 's/\#\!\/usr\/bin\/python3/\#/g' src/radexreader/__init__.py

%build
cd src
%pyproject_wheel

%install
cd src
%pyproject_install
%python_expand %fdupes %{buildroot}%{$python_sitelib}
install -Dpm 755 radexreader-cli.py %{buildroot}%{_bindir}/radexreader
install -Dpm 644 ../data/radexreader.bash %{buildroot}%{_datadir}/bash-completion/completions/radexreader
install -Dpm 644 ../data/radexreader.1 %{buildroot}%{_mandir}/man1/radexreader.1
install -Dpm 644 ../data/radexreader.fr.1 %{buildroot}%{_mandir}/fr/man1/radexreader.1
%python_clone -a %{buildroot}%{_bindir}/radexreader
%python_clone -a %{buildroot}%{_datadir}/bash-completion/completions/radexreader
%python_clone -a %{buildroot}%{_mandir}/man1/radexreader.1
%python_clone -a %{buildroot}%{_mandir}/fr/man1/radexreader.1
%python_expand install -Dpm 644 ../scripts/debian/python3-radexreader.udev %{buildroot}%{_udevrulesdir}/60-python%{$python_bin_suffix}-radexreader.rules

%files %{python_files}
%license LICENSE
%doc README.md
%{python_sitelib}/radexreader
%{python_sitelib}/radexreader-%{version}.dist-info
%python_alternative %{_bindir}/radexreader
%python_alternative %{_datadir}/bash-completion/completions/radexreader
%python_alternative %{_mandir}/man1/radexreader.1%{?ext_man}
%python_alternative %{_mandir}/fr/man1/radexreader.1%{?ext_man}
%{_udevrulesdir}/60-python%{python_bin_suffix}-radexreader.rules

%post
%{python_install_alternative radexreader radexreader.1}

%postun
%{python_uninstall_alternative radexreader radexreader.1}


%changelog
* Fri Aug 08 2025 Fabrice Creuzot <code@luigifab.fr> - 1.3.0-1
- New upstream release

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
- New upstream release

* Sun Apr 04 2021 Fabrice Creuzot <code@luigifab.fr> - 1.1.0-1
- Initial openSUSE package release
