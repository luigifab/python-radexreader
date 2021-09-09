%{?!python_module:%define python_module() python-%{**} python3-%{**}}
Name:          python-radexreader
Version:       1.2.1
Release:       0
Summary:       Reader for the RADEX RD1212 and ONE Geiger counters
License:       GPL-2.0-or-later
URL:           https://github.com/luigifab/python-radexreader
Source0:       %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:     noarch
BuildRequires: %{python_module setuptools}
BuildRequires: %{python_module pyserial}
BuildRequires: %{python_module pyusb}
BuildRequires: python-rpm-macros
BuildRequires: fdupes
Requires:      python-pyserial
Requires:      python-pyusb
Requires(post):   update-alternatives
Requires(postun): update-alternatives

%python_subpackages

%description
The RadexReader is an user-space driver for the RADEX RD1212 and
the RADEX ONE Geiger counters. It allow to read and clear stored
data via USB.

To avoid Access denied (insufficient permissions), don't forget
to unplug the device after installation.


%prep
%setup -q -n python-radexreader-%{version}
sed -i 's/python3-radexreader /python3-radexreader-rpm /g' src/radexreader.py
sed -i 's/\#\!\/usr\/bin\/python3/\#/g' src/radexreader/__init__.py

%build
cd src
%python_build

%install
cd src
%python_install
%python_expand %fdupes %{buildroot}%{$python_sitelib}
mkdir -p %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_udevrulesdir}/
%python_expand install -p -m 644 ../debian/udev %{buildroot}%{_udevrulesdir}/60-python%{$python_bin_suffix}-radexreader.rules
install -p -m 755 ../src/radexreader.py %{buildroot}%{_bindir}/radexreader
%python_clone -a %{buildroot}%{_bindir}/radexreader

%files %{python_files}
%license LICENSE
%doc README.md
%python_alternative %{_bindir}/radexreader
%{python_sitelib}/radexreader/
%{python_sitelib}/radexreader*egg-info/
%{_udevrulesdir}/60-python%{python_bin_suffix}-radexreader.rules

%post
%python_install_alternative radexreader

%postun
%python_uninstall_alternative radexreader


%changelog
* Thu Sep 09 2021 Fabrice Creuzot <code@luigifab.fr> - 1.2.1-1
- New upstream version

* Wed May 05 2021 Fabrice Creuzot <code@luigifab.fr> - 1.2.0-1
- New upstream version

* Sun Apr 04 2021 Fabrice Creuzot <code@luigifab.fr> - 1.1.0-1
- Initial openSUSE package release
