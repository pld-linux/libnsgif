#
# Conditional build:
%bcond_without	static_libs	# don't build static library

Summary:	Decoding library for the GIF format
Summary(pl.UTF-8):	Biblioteka dekodująca pliki w formacie GIF
Name:		libnsgif
Version:	0.1.2
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://download.netsurf-browser.org/libs/releases/%{name}-%{version}-src.tar.gz
# Source0-md5:	2217255323e85dc3c0a295e1fcca9e05
Patch0:		no-Werror.patch
URL:		http://www.netsurf-browser.org/projects/libnsgif/
BuildRequires:	netsurf-buildsystem >= 1.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libnsgif is a decoding library for the GIF image file format, written
in C. It was developed as part of the NetSurf project and is available
for use by other software under the MIT licence.

%description -l pl.UTF-8
Libnsgif to napisana w C biblioteka dekodująca pliki obrazów w
formacie GIF. Powstała jako część projektu NetSurf i jest dostępna do
wykorzystania przez inne programy na licencji MIT.

%package devel
Summary:	libsgif library headers
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libnsgif
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the include files and other resources you can
use to incorporate libnsgif into applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe pozwalające na używanie biblioteki libnsgif w swoich
programach.

%package static
Summary:	libnsgif static library
Summary(pl.UTF-8):	Statyczna biblioteka libnsgif
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This is package with static libnsgif library.

%description static -l pl.UTF-8
Statyczna biblioteka libnsgif.

%prep
%setup -q
%patch0 -p1

%build
export CC="%{__cc}"
export CFLAGS="%{rpmcflags}"
export LDFLAGS="%{rpmldflags}"

%{__make} \
	Q= \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-shared

%if %{with static_libs}
%{__make} \
	Q= \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-static
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-shared \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} install \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-static \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING
%attr(755,root,root) %{_libdir}/libnsgif.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnsgif.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnsgif.so
%{_includedir}/libnsgif.h
%{_pkgconfigdir}/libnsgif.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libnsgif.a
%endif
