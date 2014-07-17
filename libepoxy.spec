%bcond_without	tests
Summary:	Direct Rendering Manager runtime library
Name:		libepoxy
Version:	1.2
Release:	1
License:	MIT
Group:		X11/Libraries
URL:		http://github.com/anholt/libepoxy
Source0:	https://github.com/anholt/libepoxy/archive/v%{version}.tar.gz
# Source0-md5:	12d6b7621f086c0c928887c27d90bc30
BuildRequires:	Mesa-libEGL-devel
BuildRequires:	Mesa-libGL-devel
BuildRequires:	autoconf
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	python3
BuildRequires:	xorg-util-util-macros

%description
A library for handling OpenGL function pointer management.

%package devel
Summary:	Development files for libepoxy
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains libraries and header files for developing
applications that use %{name}.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules

%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %ghost %{_libdir}/libepoxy.so.0
%attr(755,root,root) %{_libdir}/libepoxy.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libepoxy.so
%{_includedir}/epoxy
%{_pkgconfigdir}/epoxy.pc
