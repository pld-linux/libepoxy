#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	tests		# test suite
%bcond_without	static_libs	# static library build

Summary:	Epoxy - GL dispatch library
Summary(pl.UTF-8):	Epoxy - biblioteka do przekazywania funkcji GL
Name:		libepoxy
Version:	1.5.5
Release:	1
License:	MIT
Group:		Libraries
##Source0Download: https://github.com/anholt/libepoxy/releases
#Source0:	https://github.com/anholt/libepoxy/releases/download/v1.4/%{name}-%{version}.tar.xz
Source0:	https://download.gnome.org/sources/libepoxy/1.5/%{name}-%{version}.tar.xz
# Source0-md5:	516ff05a42157c86e32c6598321737af
URL:		https://github.com/anholt/libepoxy
%{?with_tests:BuildRequires:	Mesa-khrplatform-devel}
BuildRequires:	Mesa-libEGL-devel
BuildRequires:	Mesa-libGL-devel
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	meson
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-util-util-macros >= 1.8
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Epoxy is a library for handling OpenGL function pointer management for
you.

%description -l pl.UTF-8
Epoxy to biblioteka do obsługi zarządzania wskaźnikami do funkcji
OpenGL.

%package devel
Summary:	Development files for libepoxy
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libepoxy
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files for developing applications
that use libepoxy.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących bibliotekę libepoxy.

%package static
Summary:	Static libepoxy library
Summary(pl.UTF-8):	Statyczna biblioteka libepoxy
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libepoxy library.

%description static -l pl.UTF-8
Statyczna biblioteka libepoxy.

%package apidocs
Summary:	API documentation for libepoxy library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libepoxy
Group:		Documentation
%{?noarchpackage}

%description apidocs
API documentation for libepoxy library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libepoxy.

%prep
%setup -q

%build
%meson build \
	%{!?with_static_libs:--default-library=shared} \
	%{?with_apidocs:-Ddocs=true} \
	%{!?with_tests:-Dtests=false}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README.md
%attr(755,root,root) %{_libdir}/libepoxy.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libepoxy.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libepoxy.so
%{_includedir}/epoxy
%{_pkgconfigdir}/epoxy.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libepoxy.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_docdir}/epoxy
%endif
