Name:		gnome-online-accounts
Version:	3.14.4
Release:	3%{?dist}
Summary:	Single sign-on framework for GNOME

Group:		System Environment/Libraries
License:	LGPLv2+
URL:		https://live.gnome.org/GnomeOnlineAccounts
Source0:	http://download.gnome.org/sources/gnome-online-accounts/3.14/%{name}-%{version}.tar.xz

Patch0:		translations.patch
Patch1:		0001-daemon-Don-t-leak-the-GoaProvider.patch
Patch2:		kerberos-smartcard.patch
Patch3:		kerberos-separate-process.patch
Patch4:		ensure-credentials-startup-and-network-change.patch
Patch5:		kerberos-fix-renewal.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gcr-devel
BuildRequires:	glib2-devel >= 2.35
BuildRequires:	gtk3-devel >= 3.5.1
BuildRequires:	gnome-common
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	krb5-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	webkitgtk3-devel
BuildRequires:	json-glib-devel
BuildRequires:	libsecret-devel >= 0.7
BuildRequires:	libsoup-devel >= 2.41
BuildRequires:	rest-devel
BuildRequires:	telepathy-glib-devel
BuildRequires:	libxml2-devel

Requires:	realmd

%description
GNOME Online Accounts provides interfaces so that applications and libraries
in GNOME can access the user's online accounts. It has providers for Google,
ownCloud, Facebook, Flickr, Windows Live, Pocket, Microsoft Exchange,
IMAP/SMTP, Jabber, SIP and Kerberos.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	gobject-introspection-devel

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p1 -b .translations
%patch1 -p1 -b .provider-leak
%patch2 -p1 -b .kerberos-smartcard
%patch3 -p1 -b .kerberos-separate-process
%patch4 -p1 -b .ensure-credentials
%patch5 -p1 -b .kerberos-fix-renewal

%build
autoreconf --force --install
%configure \
  --disable-static \
  --enable-gtk-doc \
  --enable-exchange \
  --disable-facebook \
  --enable-flickr \
  --enable-google \
  --enable-imap-smtp \
  --enable-kerberos \
  --enable-owncloud \
  --enable-pocket \
  --enable-telepathy \
  --enable-windows-live
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la $RPM_BUILD_ROOT/%{_libdir}/control-center-1/panels/*.la

%find_lang %{name}
%find_lang %{name}-tpaw

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

%files -f %{name}.lang -f %{name}-tpaw.lang
%doc NEWS COPYING
%{_libdir}/girepository-1.0/Goa-1.0.typelib
%{_libdir}/libgoa-1.0.so.0
%{_libdir}/libgoa-1.0.so.0.0.0
%{_libdir}/libgoa-backend-1.0.so.1
%{_libdir}/libgoa-backend-1.0.so.1.0.0
%{_prefix}/libexec/goa-daemon
%{_prefix}/libexec/goa-identity-service
%{_datadir}/dbus-1/services/org.gnome.OnlineAccounts.service
%{_datadir}/dbus-1/services/org.gnome.Identity.service
%{_datadir}/icons/hicolor/*/apps/goa-*.png
%{_datadir}/icons/hicolor/*/apps/im-*.png
%{_datadir}/icons/hicolor/*/apps/im-*.svg
%{_datadir}/man/man8/goa-daemon.8.gz
%{_datadir}/glib-2.0/schemas/org.gnome.online-accounts.gschema.xml

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/goawebview.css
%{_datadir}/%{name}/irc-networks.xml

%files devel
%{_includedir}/goa-1.0/
%{_libdir}/libgoa-1.0.so
%{_libdir}/libgoa-backend-1.0.so
%{_datadir}/gir-1.0/Goa-1.0.gir
%{_libdir}/pkgconfig/goa-1.0.pc
%{_libdir}/pkgconfig/goa-backend-1.0.pc
%{_datadir}/gtk-doc/html/goa/

%dir %{_libdir}/goa-1.0
%{_libdir}/goa-1.0/include

%changelog
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

