Name:		libpaper
Version:	1.1.23
Release:	6.1%{?dist}
Summary:	Library and tools for handling papersize
Group:		System Environment/Libraries
License:	GPLv2
URL:		http://packages.qa.debian.org/libp/libpaper.html
Source0:	http://ftp.debian.org/debian/pool/main/libp/libpaper/%{name}_%{version}+nmu1.tar.gz
# Filed	upstream as:
# http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=496126
Patch0:		libpaper-1.1.20-automake_1.10.patch
# Upstream bug:
# http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=475683
Patch1:		libpaper-1.1.23-debianbug475683.patch
# Filed upstream as:
# http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=481213
Patch2:		libpaper-useglibcfallback.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	libtool, gettext, gawk

%description
The paper library and accompanying files are intended to provide a 
simple way for applications to take actions based on a system- or 
user-specified paper size. This release is quite minimal, its purpose 
being to provide really basic functions (obtaining the system paper name 
and getting the height and width of a given kind of paper) that 
applications can immediately integrate.

%package devel
Summary:	Headers/Libraries for developing programs that use libpaper
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains headers and libraries that programmers will need 
to develop applications which use libpaper.

%prep
%setup -q -n %{name}-%{version}+nmu1
%patch0 -p1 -b .automake110
%patch1 -p1 -b .dlfix
%patch2 -p1 -b .useglibcfallback
libtoolize

%build
touch AUTHORS NEWS
aclocal
autoconf
automake -a
%configure --disable-static
# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/*.la
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
echo '# Simply write the paper name. See papersize(5) for possible values' > $RPM_BUILD_ROOT%{_sysconfdir}/papersize
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/libpaper.d
for i in cs da de es fr gl hu it ja nl pt_BR sv tr uk vi; do
	mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale/$i/LC_MESSAGES/;
	msgfmt debian/po/$i.po -o $RPM_BUILD_ROOT%{_datadir}/locale/$i/LC_MESSAGES/%{name}.mo;
done
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-, root, root, -)
%doc COPYING ChangeLog README
%config(noreplace) %{_sysconfdir}/papersize
%dir %{_sysconfdir}/libpaper.d
%{_bindir}/paperconf
%{_libdir}/libpaper.so.*
%{_sbindir}/paperconfig
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%files devel
%defattr(-, root, root, -)
%{_includedir}/paper.h
%{_libdir}/libpaper.so
%{_mandir}/man3/*

%changelog
* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.1.23-6.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.23-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1.23-4
- run libtoolize to fix build with newer libtool
- disable rpath

* Fri Aug 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1.23-3
- update to nmu1
- apply patch to fix imprecise definition of DL format
- apply patch so that when no config is present, libpaper will fallback through
  LC_PAPER before giving up and using Letter

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.23-2
- Autorebuild for GCC 4.3

* Tue Feb 19 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.1.23-1
- 1.1.23

* Fri Aug 24 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.1.22-1.1
- missing BR: gawk

* Thu Aug 23 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.1.22-1
- bump, no real changes of note, rebuild for ppc32
- license fix, v2 only

* Mon Jul 09 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.1.21-1.1
- BR: libtool

* Mon Jul 09 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.1.21-1
- bump to 1.1.21
- fix automake bug (bz 247458)

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 1.1.20-5
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Sat Sep 23 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.1.20-4
- remove aclocal call

* Sat Sep 23 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.1.20-3
- fix FC-4 with aclocal call
- move man3 pages to -devel
- don't set default, just put comment in conf file
- own /etc/libpaper.d
- use debian/NEWS
- include the meager translations
- use --disable-static

* Sat Sep 23 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.1.20-2
- nuke static lib
- own /etc/papersize
- fix mixed spaces/tabs rpmlint warning

* Sat Sep 23 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.1.20-1
- initial package for Fedora Extras
