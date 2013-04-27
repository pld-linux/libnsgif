#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	Decoding library for the GIF format
Name:		libnsgif
Version:	0.1.0
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://download.netsurf-browser.org/libs/releases/%{name}-%{version}-src.tar.gz
# Source0-md5:	f3d4295be77db30da1f4167b270bb4d9
URL:		http://www.netsurf-browser.org/projects/libnsgif/
BuildRequires:	netsurf-buildsystem
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libnsgif is a decoding library for the GIF image file format, written
in C. It was developed as part of the NetSurf project and is available
for use by other software under the MIT licence.

%package devel
Summary:	libsgif library headers
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libnsgif
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This is the libraries, include files and other resources you can use
to incorporate libnsgif into applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe pozwalające na używanie biblioteki libnsgif w swoich
programach.

%package static
Summary:	libnsgif static libraries
Summary(pl.UTF-8):	Statyczne biblioteki libnsgif
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This is package with static libnsgif libraries.

%description static -l pl.UTF-8
Statyczna biblioteka libnsgif.

%prep
%setup -q

%build
%{__make} PREFIX=%{_prefix} COMPONENT_TYPE=lib-shared Q='' \
	CFLAGS="%{rpmcflags}" LDFLAGS="%{rpmldflags}"
%if %{with static_libs}
%{__make} PREFIX=%{_prefix} COMPONENT_TYPE=lib-static Q='' \
	CFLAGS="%{rpmcflags}" LDFLAGS="%{rpmldflags}"
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-shared

%if %{with static_libs}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-static
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*.h
%{_pkgconfigdir}/*pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif
