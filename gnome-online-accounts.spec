%global gettext_version 0.19.8
%global glib2_version 2.52
%global gtk3_version 3.19.12
%global libsoup_version 2.42
%global webkit2gtk3_version 2.12.0

Name:		gnome-online-accounts
Version:	3.28.0
Release:	1%{?dist}
Summary:	Single sign-on framework for GNOME

License:	LGPLv2+
URL:		https://wiki.gnome.org/Projects/GnomeOnlineAccounts
Source0:	https://download.gnome.org/sources/gnome-online-accounts/3.28/%{name}-%{version}.tar.xz

BuildRequires:	pkgconfig(gcr-3)
BuildRequires:	pkgconfig(gio-2.0) >= %{glib2_version}
BuildRequires:	pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires:	pkgconfig(gobject-2.0) >= %{glib2_version}
BuildRequires:	pkgconfig(gtk+-3.0) >= %{gtk3_version}
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	gettext >= %{gettext_version}
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	krb5-devel
BuildRequires:	pkgconfig(webkit2gtk-4.0) >= %{webkit2gtk3_version}
BuildRequires:	pkgconfig(json-glib-1.0)
BuildRequires:	pkgconfig(libsecret-1) >= 0.7
BuildRequires:	pkgconfig(libsoup-2.4) >= %{libsoup_version}
BuildRequires:	pkgconfig(rest-0.7)
%if ! 0%{?fedora} && 0%{?rhel} <= 7
BuildRequires:	pkgconfig(telepathy-glib)
%endif
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	vala

Requires:	gettext-libs%{?isa} >= %{gettext_version}
Requires:	glib2%{?_isa} >= %{glib2_version}
Requires:	gtk3%{?_isa} >= %{gtk3_version}
Requires:	libsoup%{?_isa} >= %{libsoup_version}
Requires:	webkitgtk4%{?_isa} >= %{webkit2gtk3_version}

%description
GNOME Online Accounts provides interfaces so that applications and libraries
in GNOME can access the user's online accounts. It has providers for Google,
ownCloud, Facebook, Flickr, Foursquare, Microsoft Account, Pocket, Microsoft
Exchange, IMAP/SMTP and Kerberos.

%package devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure \
  --disable-lastfm \
  --disable-media-server \
  --disable-silent-rules \
  --disable-static \
  --disable-todoist \
%if ! 0%{?fedora} && 0%{?rhel} <= 7
  --disable-facebook \
  --disable-foursquare \
  --enable-telepathy \
%else
  --disable-telepathy \
  --enable-facebook \
  --enable-foursquare \
%endif
  --enable-exchange \
  --enable-flickr \
  --enable-google \
  --enable-gtk-doc \
  --enable-imap-smtp \
  --enable-kerberos \
  --enable-owncloud \
  --enable-pocket \
  --enable-windows-live
%make_build

%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -delete

%find_lang %{name}

%if ! 0%{?fedora} && 0%{?rhel} <= 7
%find_lang %{name}-tpaw
%endif

%post
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%if ! 0%{?fedora} && 0%{?rhel} <= 7
%files -f %{name}.lang -f %{name}-tpaw.lang
%else
%files -f %{name}.lang
%endif

%license COPYING
%doc COPYING
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/Goa-1.0.typelib
%{_libdir}/libgoa-1.0.so.0
%{_libdir}/libgoa-1.0.so.0.0.0
%{_libdir}/libgoa-backend-1.0.so.1
%{_libdir}/libgoa-backend-1.0.so.1.0.0
%dir %{_libdir}/goa-1.0
%dir %{_libdir}/goa-1.0/web-extensions
%{_libdir}/goa-1.0/web-extensions/libgoawebextension.so
%{_prefix}/libexec/goa-daemon
%{_prefix}/libexec/goa-identity-service
%{_datadir}/dbus-1/services/org.gnome.OnlineAccounts.service
%{_datadir}/dbus-1/services/org.gnome.Identity.service
%{_datadir}/icons/hicolor/*/apps/goa-*.png
%{_datadir}/man/man8/goa-daemon.8.gz
%{_datadir}/glib-2.0/schemas/org.gnome.online-accounts.gschema.xml

%if ! 0%{?fedora} && 0%{?rhel} <= 7
%{_datadir}/icons/hicolor/*/apps/im-*.png
%{_datadir}/icons/hicolor/*/apps/im-*.svg

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/irc-networks.xml
%endif

%files devel
%{_includedir}/goa-1.0/
%{_libdir}/libgoa-1.0.so
%{_libdir}/libgoa-backend-1.0.so
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Goa-1.0.gir
%{_libdir}/pkgconfig/goa-1.0.pc
%{_libdir}/pkgconfig/goa-backend-1.0.pc
%{_datadir}/gtk-doc/html/goa/
%{_libdir}/goa-1.0/include
%{_datadir}/vala/

%changelog
* Thu Mar 15 2018 Kalev Lember <klember@redhat.com> - 3.28.0-1
- Update to 3.28.0
- Resolves: #1568177

* Tue Dec 19 2017 Debarshi Ray <rishi@fedoraproject.org> - 3.26.2-1
- Update to 3.26.2
Resolves: #1525963

* Thu Oct 26 2017 Debarshi Ray <rishi@fedoraproject.org> - 3.26.1-2
- Backport fix for adding multiple accounts of the same type (GNOME #781005)
Resolves: #1503726

* Wed Oct 18 2017 Debarshi Ray <rishi@fedoraproject.org> - 3.26.1-1
- Update to 3.26.1
Resolves: #1503726

* Fri Mar 10 2017 Debarshi Ray <rishi@fedoraproject.org> - 3.22.5-1
- Update to 3.22.5
Resolves: #1386953, #1430813

* Wed Mar 08 2017 Debarshi Ray <rishi@fedoraproject.org> - 3.22.4-2
- Don't change the list of enabled providers
Resolves: #1386953

* Thu Feb 16 2017 Kalev Lember <klember@redhat.com> - 3.22.4-1
- Update to 3.22.4
Resolves: #1386953

* Tue Aug 23 2016 Debarshi Ray <rishi@fedoraproject.org> - 3.14.5-5
- Ensure that temporary accounts are really removed from the keyring and
  avoid a WARNING
Resolves: #1261940

* Wed Aug 10 2016 Debarshi Ray <rishi@fedoraproject.org> - 3.14.5-4
- Fail early on Kerberos ticket request when ticketing is disabled
Resolves: #1364705

* Mon Jun 13 2016 Debarshi Ray <rishi@fedoraproject.org> - 3.14.5-3
- Don't remove Telepathy accounts or expire Kerberos credentials when stopping
  goa-daemon
Resolves: #1267534

* Wed May 18 2016 Debarshi Ray <rishi@fedoraproject.org> - 3.14.5-2
- Don't let temporary accounts accumulate in accounts.conf and the keyring
Resolves: #1261940

* Mon Mar 14 2016 Debarshi Ray <rishi@fedoraproject.org> - 3.14.5-1
- Update to 3.14.5
- Rebase downstream patches
Resolves: #1310832

* Tue Sep 22 2015 Ray Strode <rstrode@redhat.com> 3.14.4-3
- Fix kerberos renewal for KDCs that support it
Resolves: #1189888

* Mon Jun 08 2015 Debarshi Ray <rishi@fedoraproject.org> - 3.14.4-2
- Use newer WebKit
- Refresh the credentials during startup and network changes
Resolves: #1174600, #1189888

* Tue May 05 2015 Debarshi Ray <rishi@fedoraproject.org> - 3.14.4-1
- Update to 3.14.4
- Disable Facebook
Resolves: #1174600

* Mon Mar 23 2015 Richard Hughes <rhughes@redhat.com> - 3.14.3-1
- Update to 3.14.3
Resolves: #1174600

* Fri May 23 2014 Ray Strode <rstrode@redhat.com> 3.8.5-9.1
- Bump for dist tag confusion
Related: #1096399

* Fri May 09 2014 Ray Strode <rstrode@redhat.com> 3.8.5-8.1
- Fix various resource leaks in the kerberos code
Resolves: #1096399

* Mon Mar 31 2014 Debarshi Ray <rishi@fedoraproject.org> - 3.8.5-8
- Popup is too small to display Facebook authorization
Resolves: #1081520

* Fri Feb 28 2014 Matthias Clasen <mclasen@redhat.com> - 3.8.5-7
- Turn off silent builds and make them verbose
Resolves: #1070809

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 3.8.5-6
- Mass rebuild 2014-01-24

* Tue Jan 07 2014 Debarshi Ray <rishi@fedoraproject.org> - 3.8.5-5
- Don't offer a PasswordBased interface for Google
Resolves: #1049337

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.8.5-4
- Mass rebuild 2013-12-27

* Wed Dec 11 2013 Matthias Clasen <mclasen@redhat.com> 3.8.5-3
- Update translations
Resolves: #1030343

* Wed Nov 06 2013 Ray Strode <rstrode@redhat.com> 3.8.5-2
- Fix kerberos crash when user manually erases stored credentials with seahorse
Resolves: #1027413

* Wed Nov 06 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.8.5-1
- Update to 3.8.5
Resolves: #1023117, #1027258

* Fri Nov 01 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.8.4.1-2
- Support libkrb5's new kernel keyring based credentials cache
Resolves: #991184

* Tue Oct 08 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.8.4.1-1
- Update to 3.8.4.1

* Fri Aug 30 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.8.3-1
- Update to 3.8.3

* Tue Jul  2 2013 Matthias Clasen <mclasen@redhat.com> - 3.8.2-2
- Rebuild with newer gtk-doc to fix multilib issue

* Mon May 13 2013 Matthias Clasen <mclasen@redhat.com> - 3.8.2-1
- Update to 3.8.2

* Mon Apr 15 2013 Richard Hughes <rhughes@redhat.com> - 3.8.1-1
- Update to 3.8.1

* Tue Mar 26 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.8.0-1
- Update to 3.8.0

* Wed Mar 20 2013 Richard Hughes <rhughes@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Tue Mar 05 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.7.91-1
- Update to 3.7.91

* Tue Feb 26 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.7.90-2
- Enable IMAP / SMTP

* Fri Feb 22 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.90-1
- Update to 3.7.90

* Wed Feb 06 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.7.5-1
- Update to 3.7.5

* Wed Feb 06 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.4-2
- Rebuilt for libgcr soname bump

* Mon Jan 14 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.7.4-1
- Update to 3.7.4

* Thu Jan 03 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.7.3-1
- Update to 3.7.3

* Sun Nov 18 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.7.2-1
- Update to 3.7.2

* Tue Oct 23 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.7.1-1
- Update to 3.7.1

* Mon Oct 15 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.6.1-1
- Update to 3.6.1

* Tue Sep 25 2012 Matthias Clasen <mclasen@redhat.com> - 3.6.0-1
- Update to 3.6.0

* Mon Sep 17 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.5.92-1
- Update to 3.5.92

* Tue Sep 04 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.5.91-1
- Update to 3.5.91

* Tue Aug 21 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.5.90-1
- Update to 3.5.90

* Tue Aug 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.5-1
- Update to 3.5.5

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.5.4-1
- Update to 3.5.4

* Mon Jun 25 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.5.3-1
- Update to 3.5.3

* Tue Jun 05 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.5.2-1
- Update to 3.5.2

* Wed May 02 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.5.1-1
- Update to 3.5.1

* Tue Apr 17 2012 Richard Hughes <hughsient@gmail.com> - 3.4.1-1
- Update to 3.4.1

* Mon Mar 26 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.4.0-1
- Update to 3.4.0

* Wed Mar 21 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.3.92.1-1
- Update to 3.3.92.1

* Tue Mar 20 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.3.92-1
- Update to 3.3.92

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 19 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.3.0-2
- Enable Windows Live provider.

* Mon Dec 19 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.3.0-1
- Update to 3.3.0.
- Update source url.

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for glibc bug#747377

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Wed Sep 28 2011 Ray <rstrode@redhat.com> - 3.2.0.1-1
- Update to 3.2.0.1

* Mon Sep 26 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.91-1
- Update to 3.1.91

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.90-1
- Update to 3.1.90

* Fri Jul 01 2011 Bastien Nocera <bnocera@redhat.com> 3.1.1-1
- Update to 3.1.1

* Tue Jun 14 2011 Bastien Nocera <bnocera@redhat.com> 3.1.0-3
- Add more necessary patches

* Tue Jun 14 2011 Bastien Nocera <bnocera@redhat.com> 3.1.0-2
- Update with review comments from Peter Robinson

* Mon Jun 13 2011 Bastien Nocera <bnocera@redhat.com> 3.1.0-1
- First version

