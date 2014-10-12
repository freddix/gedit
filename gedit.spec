Summary:	GNOME text editor
Name:		gedit
Version:	3.14.0
Release:	1
License:	GPL v2
Group:		X11/Applications/Editors
Source0:	http://ftp.gnome.org/pub/gnome/sources/gedit/3.14/%{name}-%{version}.tar.xz
# Source0-md5:	fae6439f950bf3f00101a16c2c924bdf
URL:		https://wiki.gnome.org/Apps/Gedit
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	enchant-devel
BuildRequires:	gettext-devel
BuildRequires:	gobject-introspection-devel >= 1.42.0
BuildRequires:	gsettings-desktop-schemas-devel >= 3.14.0
BuildRequires:	gtk+3-devel >= 3.14.0
BuildRequires:	gtk-doc
BuildRequires:	gtksourceview3-devel >= 3.14.0
BuildRequires:	intltool
BuildRequires:	iso-codes
BuildRequires:	libpeas-gtk-devel
BuildRequires:	libtool
BuildRequires:	pkg-config
BuildRequires:	python-pygobject3-devel >= 3.14.0
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib-gio-gsettings
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}

%description
gedit is a small but powerful text editor for GTK+ and/or GNOME. It
includes such features as split-screen mode, a plugin API, which
allows gedit to be extended to support many features while remaining
small at its core, multiple document editing and many more functions.

%package plugins-python3
Summary:	Gedit plugins written in Python
Group:		Applications
Requires:	%{name} = %{version}-%{release}
Requires:	libpeas-loader-python3
Requires:	python3-pycairo

%description plugins-python3
Gedit plugins written in Python.

%package libs
Summary:	gedit libraries
Group:		X11/Libraries

%description libs
gedit libraries.

%package devel
Summary:	gedit header files
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
gedit header files

%package apidocs
Summary:	gedit API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
gedit API documentation.

%prep
%setup -q

# kill gnome common deps
%{__sed} -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' configure.ac

%build
%{__libtoolize}
%{__intltoolize}
%{__aclocal} -I m4 -I libgd
%{__autoconf}
%{__automake}
%configure \
	--disable-schemas-compile	\
	--disable-silent-rules		\
	--disable-updater		\
	--enable-python			\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/gedit/{,plugins/}*.la
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/GConf

%py_postclean

%find_lang gedit --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%update_gsettings_cache

%postun
%update_desktop_database_postun
%update_gsettings_cache

%post plugins-python3
%update_gsettings_cache

%postun plugins-python3
%update_gsettings_cache

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f gedit.lang
%defattr(644,root,root,755)
%doc README ChangeLog AUTHORS
%dir %{_libdir}/gedit/plugins
%attr(755,root,root) %{_bindir}/gedit
%attr(755,root,root) %{_bindir}/gnome-text-editor
%attr(755,root,root) %{_libdir}/gedit/plugins/*.so
%{_libdir}/gedit/plugins/docinfo.plugin
%{_libdir}/gedit/plugins/filebrowser.plugin
%{_libdir}/gedit/plugins/modelines.plugin
%{_libdir}/gedit/plugins/sort.plugin
%{_libdir}/gedit/plugins/spell.plugin
%{_libdir}/gedit/plugins/time.plugin
%{_datadir}/gedit
%{_datadir}/dbus-1/services/org.gnome.gedit.service
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.filebrowser.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.filebrowser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.time.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.time.gschema.xml
%{_desktopdir}/org.gnome.gedit.desktop
%{_mandir}/man1/gedit.1*

%files plugins-python3
%defattr(644,root,root,755)
%dir %{_libdir}/gedit/plugins/externaltools
%dir %{_libdir}/gedit/plugins/pythonconsole
%dir %{_libdir}/gedit/plugins/quickopen
%dir %{_libdir}/gedit/plugins/snippets
%{_libdir}/gedit/plugins/externaltools.plugin
%{_libdir}/gedit/plugins/externaltools/*.py
%{_libdir}/gedit/plugins/externaltools/__pycache__
%{_libdir}/gedit/plugins/pythonconsole.plugin
%{_libdir}/gedit/plugins/pythonconsole/*py
%{_libdir}/gedit/plugins/pythonconsole/__pycache__
%{_libdir}/gedit/plugins/quickopen.plugin
%{_libdir}/gedit/plugins/quickopen/*.py
%{_libdir}/gedit/plugins/quickopen/__pycache__
%{_libdir}/gedit/plugins/snippets.plugin
%{_libdir}/gedit/plugins/snippets/*.py
%{_libdir}/gedit/plugins/snippets/__pycache__
%{py3_sitedir}/gi/overrides/*.py
%{py3_sitedir}/gi/overrides/__pycache__/*.py[co]
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.externaltools.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.pythonconsole.gschema.xml

%files libs
%defattr(644,root,root,755)
%dir %{_libdir}/gedit
%dir %{_libdir}/gedit/girepository-1.0
%attr(755,root,root) %{_libdir}/gedit/libgedit.so
%{_libdir}/gedit/girepository-1.0/Gedit-3.0.typelib

%files devel
%defattr(644,root,root,755)
%{_includedir}/gedit-3.12
%{_pkgconfigdir}/gedit.pc
%{_datadir}/vala/vapi/gedit.deps
%{_datadir}/vala/vapi/gedit.vapi

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gedit

