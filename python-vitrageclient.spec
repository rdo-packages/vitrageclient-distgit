# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%global pypi_name vitrageclient

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%{!?py_req_cleanup: %global py_req_cleanup rm -rf {,test-}requirements.txt}

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

%package -n     python%{pyver}-%{pypi_name}

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-pbr
BuildRequires:  git
BuildRequires:  python%{pyver}-iso8601
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-subunit
BuildRequires:  python%{pyver}-networkx
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-testrepository
BuildRequires:  python%{pyver}-testtools
BuildRequires:  python%{pyver}-cliff
BuildRequires:  python%{pyver}-pydot
BuildRequires:  python%{pyver}-testscenarios

Requires:       python%{pyver}-babel >= 2.3.4
Requires:       python%{pyver}-iso8601
Requires:       python%{pyver}-keystoneauth1 >= 3.4.0
Requires:       python%{pyver}-networkx
Requires:       python%{pyver}-osc-lib >= 1.10.0
Requires:       python%{pyver}-oslo-utils >= 3.33.0
Requires:       python%{pyver}-oslo-log
Requires:       python%{pyver}-pbr
Requires:       python%{pyver}-pydot
Requires:       python%{pyver}-cliff >= 2.8.0

Requires:       %{name}-bash-completion = %{version}-%{release}

Summary:        Python client for Vitrage REST API
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}}
%if %{pyver} == 3
Obsoletes: python2-%{pypi_name} < %{version}-%{release}
%endif

%description -n python%{pyver}-%{pypi_name}
%{common_desc}

# Documentation package
%package -n python-%{pypi_name}-doc
Summary:       Documentation for python client for Vitrage REST API

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-openstackdocstheme

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
%py_req_cleanup


%build
%{pyver_build}

# generate html docs
%{pyver_bin} setup.py build_sphinx -b html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}


%install
%{pyver_install}

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s vitrage %{buildroot}%{_bindir}/vitrage-%{pyver}

# push autocompletion
bashcompdir=$(pkg-config --variable=completionsdir bash-completion)
mkdir -p %{buildroot}$bashcompdir
mv %{buildroot}%{_datadir}/vitrage.bash_completion %{buildroot}$bashcompdir/vitrage

%check
export PYTHON=%{pyver_bin}
%{pyver_bin} setup.py test --slowest

%files -n python%{pyver}-%{pypi_name}
%license LICENSE
%doc README.rst
%{pyver_sitelib}/%{pypi_name}
%{pyver_sitelib}/python_%{pypi_name}-*-py?.?.egg-info
%{_bindir}/vitrage
%{_bindir}/vitrage-%{pyver}

%files -n python-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE

%files bash-completion
%license LICENSE
%{_datadir}/bash-completion/completions/vitrage

%changelog
