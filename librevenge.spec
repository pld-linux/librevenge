#
# Conditional build:
%bcond_without	static_libs	# don't build static library
%bcond_without	gdb		# GDB pretty printers

Summary:	Library for generic document converters
Summary(pl.UTF-8):	Biblioteka dla ogólnych konwerterów dokumentów
Name:		librevenge
Version:	0.0.4
Release:	1
License:	MPL v2.0 or LGPL v2.1+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/libwpd/%{name}-%{version}.tar.xz
# Source0-md5:	2677cf97716c699146f999575ac0147d
URL:		https://sourceforge.net/p/libwpd/wiki/librevenge/
BuildRequires:	autoconf >= 2.65
BuildRequires:	automake >= 1:1.11
BuildRequires:	boost-devel >= 1.20
BuildRequires:	doxygen
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
%{?with_gdb:BuildRequires:	python-modules}
BuildRequires:	rpmbuild(macros) >= 1.234
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
librevenge is a base library for writing document import filters. It
has interfaces for text documents, vector graphics, spreadsheets and
presentations.

%description -l pl.UTF-8
librevenge to biblioteka podstawowa do pisania filtrów importujących
dokumenty. Zawiera interfejsy dla dokumentów tekstowych, grafiki
wektorowej, arkuszy kalkulacyjnych oraz prezentacji.

%package devel
Summary:	Header files for librevenge library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki librevenge
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for librevenge library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki librevenge.

%package static
Summary:	Static librevenge library
Summary(pl.UTF-8):	Statyczna biblioteka librevenge
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static librevenge library.

%description static -l pl.UTF-8
Statyczna biblioteka librevenge.

%package apidocs
Summary:	API documentation for librevenge library
Summary(pl.UTF-8):	Dokumentacja API biblioteki librevenge
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for librevenge library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki librevenge.

%package gdb
Summary:	GDB Python pretty printers for librevenge types
Summary(pl.UTF-8):	Skrypty Pythona dla GDB do ładnego wypisywania typów librevenge
Group:		Development/Debuggers
Requires:	gdb

%description gdb
GDB Python pretty printers for librevenge types.

%description gdb -l pl.UTF-8
Skrypty Pythona dla GDB do ładnego wypisywania typów librevenge.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_gdb:--enable-pretty-printers} \
	%{?with_static_libs:--enable-static} \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/librevenge-*.la

%if %{with gdb}
%py_comp $RPM_BUILD_ROOT%{_datadir}/librevenge/python/librevenge
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/librevenge/python/librevenge
%py_postclean %{_datadir}/librevenge/python/librevenge
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/librevenge-0.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librevenge-0.0.so.0
%attr(755,root,root) %{_libdir}/librevenge-generators-0.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librevenge-generators-0.0.so.0
%attr(755,root,root) %{_libdir}/librevenge-stream-0.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librevenge-stream-0.0.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librevenge-0.0.so
%attr(755,root,root) %{_libdir}/librevenge-generators-0.0.so
%attr(755,root,root) %{_libdir}/librevenge-stream-0.0.so
%{_includedir}/librevenge-0.0
%{_pkgconfigdir}/librevenge-0.0.pc
%{_pkgconfigdir}/librevenge-generators-0.0.pc
%{_pkgconfigdir}/librevenge-stream-0.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/librevenge-0.0.a
%{_libdir}/librevenge-generators-0.0.a
%{_libdir}/librevenge-stream-0.0.a
%endif

%files apidocs
%defattr(644,root,root,755)
%doc docs/doxygen/html/*

%if %{with gdb}
%files gdb
%defattr(644,root,root,755)
%{_datadir}/gdb/auto-load/%{_libdir}/librevenge-0.0.py
%{_datadir}/gdb/auto-load/%{_libdir}/librevenge-stream-0.0.py
%dir %{_datadir}/librevenge
%{_datadir}/librevenge/python
%endif
