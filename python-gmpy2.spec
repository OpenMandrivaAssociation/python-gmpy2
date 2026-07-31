%define module gmpy2
%bcond tests 1
%bcond docs 1

Name:		python-gmpy2
Version:	2.3.1
Release:	1
Source0:	https://files.pythonhosted.org/packages/source/g/gmpy2/%{module}-%{version}.tar.gz#/%{name}-%{version}.tar.gz
Summary:	General Multi-Precision arithmetic for Python 3+ (GMP, MPIR, MPFR, MPC)
URL:		https://pypi.org/project/gmpy2/
License:	LGPL-3.0-or-later
Group:		Development/Python
BuildSystem:	python

BuildRequires:	clang
BuildRequires:	llvm
BuildRequires:	make
BuildRequires:	libmpc-devel
BuildRequires:	pkgconfig(gmp)
BuildRequires:	pkgconfig(gmpxx)
BuildRequires:	pkgconfig(mpfr)
BuildRequires:	pkgconfig(python)
BuildRequires:	python >= 3.10
BuildRequires:	python%{pyver}dist(packaging)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(setuptools-scm)
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
%prep -a
# Remove bundled egg-info
rm -vrf %{module}.egg-info

# Drop setuptools version <80 constraint
sed -i 's|setuptools>=77,<80|setuptools>=77|g' pyproject.toml

%if %{with docs}
# Use local objects.inv for intersphinx
sed -e "s|\('https://docs\.python\.org/3/', \)None|\1'%{_docdir}/python-docs/objects.inv'|" \
    -i docs/conf.py
%endif

%build -p
export CFLAGS="%{optflags}"
export LDFLAGS="%{ldflags} -lpython%{pyver}"

%install -a
# The documentation needs to be built after the module is installed,
# otherwise sphinx cannot find the modules meta info.

# Make buildroot docdir
install -dpm 755 %{buildroot}%{_docdir}/%{name}
# Use sphinx-build to build html docs into buildroot docdir,
# Doc generation requires the module to be installed in order to run successfully.
PYTHONPATH="%{buildroot}%{python_sitearch}:${PWD}" \
    sphinx-build -b html docs %{buildroot}%{_docdir}/%{name}
# remove .buildinfo and .doctrees
rm -rf %{buildroot}%{_docdir}/%{name}/.buildinfo
rm -rf %{buildroot}%{_docdir}/%{name}/.doctrees

%if %{with tests}
%check
export CI=true
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="%{buildroot}%{python_sitearch}:${PWD}"
pytest test/
%endif

%files
%doc README.rst
%license COPYING COPYING.LESSER
%{python_sitearch}/%{module}
%{python_sitearch}/%{module}-%{version}.dist-info

%files doc
%{_docdir}/%{name}
