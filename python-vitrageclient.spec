%global pypi_name vitrageclient
%if 0%{?fedora}
%global with_python3 1
%else
%global with_python3 0
%endif

%if 0%{?fedora}==0
%global __python2 /usr/bin/python
%endif


%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
Python client for Vitrage REST API. Includes python library for Vitrage API \
and Command Line Interface (CLI) library.

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        Python client for Vitrage REST API

License:        ASL 2.0
URL:            http://pypi.python.org/pypi/%{name}
Source0:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch:      noarch

%description
%{common_desc}

%package -n     python2-%{pypi_name}

BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr
BuildRequires:  git
BuildRequires:  python-cliff
BuildRequires:  python-iso8601
BuildRequires:  python-mock
BuildRequires:  python-subunit
BuildRequires:  python-oslotest
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios
BuildRequires:  python-testtools

Requires:       python-babel >= 2.3.4
Requires:       python-cliff >= 2.8.0
Requires:       python-iso8601
Requires:       python-keystoneauth1 >= 3.0.1
Requires:       python-pbr
Requires:       python-osc-lib >= 1.7.0
Requires:       python-oslo-utils >= 3.20.0
Requires:       python-oslo-log

Requires:       %{name}-bash-completion = %{version}-%{release}

Summary:        Python client for Vitrage REST API
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
%{common_desc}

%if 0%{?with_python3}
# Python3 package
%package -n     python3-%{pypi_name}
Summary:        Python client for Vitrage REST API
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr >= 0.6
BuildRequires:  python3-cliff
BuildRequires:  python3-iso8601
BuildRequires:  python3-mock
BuildRequires:  python3-subunit
BuildRequires:  python3-oslotest
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools

Requires:       python3-babel >= 2.3.4
Requires:       python3-cliff >= 2.8.0
Requires:       python3-keystoneauth1 >= 3.0.1
Requires:       python3-iso8601
Requires:       python3-pbr
Requires:       python3-osc-lib >= 1.7.0
Requires:       python3-oslo-utils >= 3.20.0
Requires:       python3-oslo-log

%description -n python3-%{pypi_name}
%{common_desc}
%endif

# Documentation package
%package -n python-%{pypi_name}-doc
Summary:       Documentation for python client for Vitrage REST API

BuildRequires: python-sphinx
BuildRequires: python-openstackdocstheme

%description -n python-%{pypi_name}-doc
Documentation for python client for Vitrage REST API. Includes python library
for Vitrage API and Command Line Interface (CLI) library.

%package bash-completion
Summary:        bash completion files for vitrage
BuildRequires:  bash-completion

%description bash-completion
This package contains bash completion files for vitrage.


%prep
%autosetup -n %{name}-%{upstream_version} -S git

# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt


%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}


%install
%if 0%{?with_python3}
%py3_install
# rename python3 binary:
pushd %{buildroot}/%{_bindir}
mv vitrage vitrage-3
ln -s vitrage-3 vitrage-%{python3_version}
popd
%endif

%py2_install

# push autocompletion
bashcompdir=$(pkg-config --variable=completionsdir bash-completion)
mkdir -p %{buildroot}$bashcompdir
mv %{buildroot}%{_datadir}/vitrage.bash_completion %{buildroot}$bashcompdir/vitrage

%check
%{__python2} setup.py test --slowest

# python3 tests currently fail
%if 0%{?with_python3}
## %{__python3} setup.py test --slowest
%endif

%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/python_%{pypi_name}-*-py?.?.egg-info
%{_bindir}/vitrage

%if 0%{?with_python3}
# Files for python3
%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{_bindir}/vitrage-3
%{_bindir}/vitrage-%{python3_version}
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/python_%{pypi_name}-*-py?.?.egg-info
%endif

%files -n python-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE

%files bash-completion
%license LICENSE
%{_datadir}/bash-completion/completions/vitrage

%changelog
