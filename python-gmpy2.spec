%define module gmpy2
%bcond_without tests
%bcond_without docs

Name:		python-gmpy2
Version:	2.2.1
Release:	2
Source0:	https://files.pythonhosted.org/packages/source/g/gmpy2/%{module}-%{version}.tar.gz
Summary:	General Multi-Precision arithmetic for Python 3+ (GMP, MPIR, MPFR, MPC)
URL:		https://pypi.org/project/gmpy2/
License:	LGPL-3.0-or-later
Group:		Development/Python
BuildSystem:	python

BuildRequires:	clang
BuildRequires:	llvm
BuildRequires:	make
BuildRequires:	%{_lib}gmp-devel
BuildRequires:	%{_lib}mpc-devel
BuildRequires:	pkgconfig(mpfr)
BuildRequires:	pkgconfig(python)
BuildRequires:	python >= 3.10
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(wheel)
%if %{with tests}
BuildRequires:	python%{pyver}dist(pytest)
BuildRequires:	python%{pyver}dist(hypothesis)
BuildRequires:	python%{pyver}dist(cython)
BuildRequires:	python%{pyver}dist(mpmath)
BuildRequires:	python%{pyver}dist(numpy)
%endif
%if %{with docs}
# required as it contains local objects.inv needed for docs build
BuildRequires:	python-docs
BuildRequires:	python%{pyver}dist(sphinx)
BuildRequires:	python%{pyver}dist(sphinx-rtd-theme)
%endif
Suggests: %{name}-doc = %{version}-%{release}

%description
gmpy2 is an optimized, C-coded Python extension module that supports fast
multiple-precision arithmetic. gmpy2 is based on the original gmpy module.

gmpy2 adds support for correctly rounded multiple-precision real arithmetic
(using the MPFR library) and complex arithmetic (using the MPC library).

%package doc
License:	LGPL-3.0-or-later AND BSD-2-Clause AND MIT
Summary:	Documentation for %{name}
BuildArch:	noarch
Provides:	bundled(js-jquery)

%description doc
Documentation for %{name}.

#####################################
%prep
%autosetup -n %{module}-%{version}

# remove egg-info
rm -vrf %{module}.egg-info

%if %{with docs}
# Use local objects.inv for intersphinx
sed -e "s|\('https://docs\.python\.org/3/', \)None|\1'%{_docdir}/python-docs/objects.inv'|" \
    -i docs/conf.py
%endif

%build
export CFLAGS="%{optflags}"
%py_build

# make html docs
PYTHONPATH=$PWD/$(ls -1d build/lib.linux*) make -C docs html

%install
%py_install

%if %{with tests}
%check
export CI=true
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="%{buildroot}%{python_sitearch}:${PWD}"
pytest -v test/
%endif

%files
%{python_sitearch}/gmpy2
%{python_sitearch}/gmpy2-%{version}.dist-info
%doc README.rst
%license COPYING COPYING.LESSER

%files doc
%doc docs/_build/html/*
