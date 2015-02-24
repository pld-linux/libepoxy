#
# Conditional build:
%bcond_without	tests		# "make check" call
%bcond_without	static_libs	# static library build

Summary:	Epoxy - GL dispatch library
Summary(pl.UTF-8):	Epoxy - biblioteka do przekazywania funkcji GL
Name:		libepoxy
Version:	1.2
Release:	2
License:	MIT
Group:		Libraries
Source0:	https://github.com/anholt/libepoxy/archive/v%{version}.tar.gz
# Source0-md5:	12d6b7621f086c0c928887c27d90bc30
Patch0:		tests.patch
URL:		https://github.com/anholt/libepoxy
%{?with_tests:BuildRequires:	Mesa-khrplatform-devel}
BuildRequires:	Mesa-libEGL-devel
BuildRequires:	Mesa-libGL-devel
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	python3
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-util-util-macros >= 1.8
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

%prep
%setup -q
%ifarch x32
%patch0 -p1
%endif

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static}

%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libepoxy.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README.md
%attr(755,root,root) %ghost %{_libdir}/libepoxy.so.0
%attr(755,root,root) %{_libdir}/libepoxy.so.*.*

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
