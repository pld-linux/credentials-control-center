#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_with	gnome_cc	# GNOME Control Center panel module (needs Ubuntu patch)

Summary:	Ubuntu Online Accounts configuration panel
Summary(pl.UTF-8):	Panel konfiguracyjny Ubuntu Online Accounts
Name:		credentials-control-center
Version:	0.1.5
Release:	4
License:	LGPL v3 (libaccount-plugin), GPL v3 (panel)
Group:		Libraries
#Source0Download: https://launchpad.net/gnome-control-center-signon/
Source0:	https://launchpad.net/gnome-control-center-signon/13.04/%{version}/+download/%{name}-%{version}.tar.xz
# Source0-md5:	deaa290c89dffee5198f3f0f6f2e1fe1
Patch0:		%{name}-update.patch
URL:		https://launchpad.net/gnome-control-center-signon/
BuildRequires:	glib2-devel >= 1:2.30
%{?with_gnome_cc:BuildRequires:	gnome-control-center-devel}
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	gtk+3-devel >= 3.0.0
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	intltool >= 0.40.1
BuildRequires:	libaccounts-glib-devel >= 1.8
BuildRequires:	libsignon-glib-devel >= 1.8
BuildRequires:	pkgconfig >= 1:0.24
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	vala >= 2:0.15.1
BuildRequires:	yelp-tools
Requires:	libaccount-plugin = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package is a configuration interface for the Ubuntu Online
Accounts framework. It uses the patched GNOME Control Center in
Ubuntu, with support for external configuration panels, to show Online
Accounts settings in the Control Center. Alternatively, a standalone
credentials-preferences binary can be built, which allows
distributions without the patched GNOME Control Center to use the
configuration UI.

%description -l pl.UTF-8
Ten pakiet to interfejs konfiguracyjny do szkieletu Ubuntu Online
Accounts. Wykorzystuje załataną wersję GNOME Control Center, z obsługą
zewnętrznych paneli konfiguracyjnych, do wyświetlania ustawień Online
Accounts w Centrum Sterowania. Alternatywnie dostępny jest samodzielny
program do konfiguracji kont, który można używać jako graficzny
interfejs konfiguracyjny bez załatanego GNOME Control Center.

%package -n gnome-control-center-signon
Summary:	Ubuntu Online Accounts plugin for GNOME Control Center
Summary(pl.UTF-8):	Wtyczka Ubuntu Online Accounts dla GNOME Control Center
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n gnome-control-center-signon
Ubuntu Online Accounts credentials and settings plugin for GNOME
Control Center.

%description -n gnome-control-center-signon -l pl.UTF-8
Wtyczka konfiguracyjna danych uwierzytelniających i ustawień Ubuntu
Online Accounts dla GNOME Control Center.

%package -n libaccount-plugin
Summary:	Account plugins support library
Summary(pl.UTF-8):	Biblioteka obsługująca wtyczki dla kont
Group:		X11/Libraries
Requires:	glib2 >= 1:2.30
Requires:	gtk+3 >= 3.0.0
Requires:	libaccounts-glib >= 1.8
Requires:	libsignon-glib >= 1.8

%description -n libaccount-plugin
libaccount-plugin is an auxiliary library which provides support for
account plugins.

%description -n libaccount-plugin -l pl.UTF-8
libaccount-plugin to biblioteka pomocnicza zapewniająca obsługę
wtyczek dla kont.

%package -n libaccount-plugin-devel
Summary:	Development files for account-plugin library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki account-plugin
Group:		X11/Development/Libraries
Requires:	glib2-devel >= 1:2.30
Requires:	gtk+3-devel >= 3.0.0
Requires:	libaccount-plugin = %{version}-%{release}
Requires:	libaccounts-glib-devel >= 1.8
Requires:	libsignon-glib-devel >= 1.8

%description -n libaccount-plugin-devel
Development files for account-plugin library.

%description -n libaccount-plugin-devel -l pl.UTF-8
Pliki programistyczne biblioteki account-plugin.

%package -n libaccount-plugin-static
Summary:	Static credentials-control-center library
Summary(pl.UTF-8):	Statyczna biblioteka credentials-control-center
Group:		X11/Development/Libraries
Requires:	libaccount-plugin-devel = %{version}-%{release}

%description -n libaccount-plugin-static
Static credentials-control-center library.

%description -n libaccount-plugin-static -l pl.UTF-8
Statyczna biblioteka credentials-control-center.

%package -n libaccount-plugin-apidocs
Summary:	API documentation for account-plugin library
Summary(pl.UTF-8):	Dokumentacja API biblioteki account-plugin
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n libaccount-plugin-apidocs
API documentation for account-plugin library.

%description -n libaccount-plugin-apidocs -l pl.UTF-8
Dokumentacja API biblioteki account-plugin.

%package -n vala-libaccount-plugin
Summary:	Vala API for libaccount-plugin library
Summary(pl.UTF-8):	API języka Vala do biblioteki libaccount-plugin
Group:		X11/Development/Libraries
Requires:	libaccount-plugin-devel = %{version}-%{release}
Requires:	vala >= 2:0.15.1
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n vala-libaccount-plugin
Vala API for libaccount-plugin library.

%description -n vala-libaccount-plugin -l pl.UTF-8
API języka Vala do biblioteki libaccount-plugin.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	%{!?with_gnome_cc:--without-gnome-control-center} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/libaccount-plugin-1.0/{applications,providers}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm}	$RPM_BUILD_ROOT%{_libdir}/lib*.la
%if %{with gnome_cc}
%{__rm}	$RPM_BUILD_ROOT%{_libdir}/control-center-1/panels/lib*.la
%endif

%find_lang web-credentials --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n libaccount-plugin -p /sbin/ldconfig
%postun	-n libaccount-plugin -p /sbin/ldconfig

%files -f web-credentials.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/credentials-preferences
%attr(755,root,root) %{_bindir}/online-accounts-preferences
%attr(755,root,root) %{_libexecdir}/update-accounts
%{_datadir}/dbus-1/services/com.canonical.webcredentials.capture.service
%{_desktopdir}/credentials-preferences.desktop
%{_desktopdir}/update-accounts.desktop
%{_iconsdir}/hicolor/*x*/apps/credentials-add-account.png
%{_iconsdir}/hicolor/*x*/apps/credentials-preferences.png

%if %{with gnome_cc}
%files -n gnome-control-center-signon
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/control-center-1/panels/libcredentials.so
%{_desktopdir}/gnome-credentials-panel.desktop
%endif

%files -n libaccount-plugin
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaccount-plugin-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libaccount-plugin-1.0.so.0
%{_libdir}/girepository-1.0/AccountPlugin-1.0.typelib
%dir %{_libdir}/libaccount-plugin-1.0
%dir %{_libdir}/libaccount-plugin-1.0/applications
%dir %{_libdir}/libaccount-plugin-1.0/providers

%files -n libaccount-plugin-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaccount-plugin-1.0.so
%{_datadir}/gir-1.0/AccountPlugin-1.0.gir
%{_includedir}/libaccount-plugin
%{_pkgconfigdir}/account-plugin.pc

%if %{with static_libs}
%files -n libaccount-plugin-static
%defattr(644,root,root,755)
%{_libdir}/libaccount-plugin-1.0.a
%endif

%files -n libaccount-plugin-apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/account-plugin

%files -n vala-libaccount-plugin
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/AccountPlugin.vapi
