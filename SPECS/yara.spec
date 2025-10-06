Name:           yara
Version:        4.5.2
Release:        2%{?dist}
Summary:        Pattern matching Swiss knife for malware researchers

License:        BSD-3-Clause
VCS:            http://github.com/VirusTotal/yara/
#               http://github.com/VirusTotal/yara/releases
URL:            http://VirusTotal.github.io/yara/


%global         gituser         VirusTotal
%global         gitname         yara

# Build from git release version
Source0:        https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz


BuildRequires:  git
BuildRequires:  gcc
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  m4
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  sharutils
BuildRequires:  file
BuildRequires:  gawk
BuildRequires:  gzip
BuildRequires:  xz
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  libtool
BuildRequires:  file-devel
BuildRequires:  jansson-devel >= 2.5
BuildRequires:  openssl-devel
BuildRequires:  protobuf-c-devel
BuildRequires:  protobuf-compiler

# html doc generation
BuildRequires:  /usr/bin/sphinx-build

%description
YARA is a tool aimed at (but not limited to) helping malware researchers to
identify and classify malware samples. With YARA you can create descriptions
of malware families (or whatever you want to describe) based on textual or
binary patterns. Each description, a.k.a rule, consists of a set of strings
and a Boolean expression which determine its logic.


%package doc
Summary:        Documentation for %{name}
BuildArch:      noarch

%description doc
This package contains documentation for %{name}.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p 1 -S git
%setup -q
autoreconf --force --install


%build

# Add missing definition on RHEL7
%if 0%{?rhel} && 0%{?rhel} == 7
export CFLAGS="$CFLAGS -D PROTOBUF_C_FIELD_FLAG_ONEOF=4"
%endif

# macro %%configure already does use CFLAGS="\{optflags}" and yara build
# scripts configure/make already honors that CFLAGS
%configure --enable-magic --enable-cuckoo --enable-debug --enable-dotnet \
        --enable-macho --enable-dex --enable-pb-tests \
        --with-crypto \
        --htmldir=%{_datadir}/doc/%{name}/html
%make_build

# build the HTML documentation
pushd docs
make html
popd


%install
%make_install

# Remove static libraries
rm %{buildroot}%{_libdir}/lib%{name}.la
rm %{buildroot}%{_libdir}/lib%{name}.a

# Remove the rebuild-needed tag so it is not installed in doc pkg
rm -f %{buildroot}%{_datadir}/doc/%{name}/html/.buildinfo


%files
%license COPYING
%doc AUTHORS CONTRIBUTORS README.md
%{_bindir}/%{name}
%{_bindir}/%{name}c
%{_libdir}/lib%{name}.so.*
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}c.1*


%files devel
%{_includedir}/%{name}.h
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc


%files doc
%license COPYING
%doc docs/_build/html


%changelog
* Tue Oct 29 2024 Troy Dawson <tdawson@redhat.com> - 4.5.2-2
- Bump release for October 2024 mass rebuild:
  Resolves: RHEL-64018

* Fri Oct 25 2024 Mark Huth <mhuth@redhat.com> - 4.5.2-1
- Initial commit on c10s
- Resolves: RHEL-60383
