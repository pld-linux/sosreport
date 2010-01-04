Summary:	A set of tools to gather troubleshooting information from a system
Name:		sosreport
Version:	1.8
Release:	0.2
Group:		Applications/System
Source0:	https://fedorahosted.org/releases/s/o/sos/sos-%{version}.tar.gz
# Source0-md5:	fc841fd760558594bb189d745fc67f0c
License:	GPL v2+
URL:		http://fedorahosted.org/sos
BuildRequires:	python-devel
Patch0:		pld.patch
Patch1:		py-compiled.patch
Requires:	bzip2
Requires:	python-libxml2
Requires:	tar
Provides:	sysreport = 1.4.3-13
Obsoletes:	sysreport
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Sos is a set of tools that gathers information about system hardware
and configuration. The information can then be used for diagnostic
purposes and debugging. Sos is commonly used to help support
technicians and developers.

%prep
%setup -q -n sos-%{version}
%patch0 -p1
%patch1 -p1

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}

install -D -p gpgkeys/rhsupport.pub $RPM_BUILD_ROOT%{_datadir}/sos/rhsupport.pub
install -D -p extras/sysreport/sysreport.legacy $RPM_BUILD_ROOT%{_datadir}/sos/sysreport
ln -s sosreport $RPM_BUILD_ROOT%{_sbindir}/sysreport
%{__python} setup.py install \
	--optimize=2 \
	--skip-build \
	--root $RPM_BUILD_ROOT

%py_postclean

%find_lang sos

%clean
rm -rf $RPM_BUILD_ROOT

%files -f sos.lang
%defattr(644,root,root,755)
%doc README README.rh-upload TODO LICENSE ChangeLog
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sos.conf
%attr(755,root,root) %{_bindir}/rh-upload
%attr(755,root,root) %{_sbindir}/sosreport
%attr(755,root,root) %{_sbindir}/sysreport
%attr(755,root,root) %{_sbindir}/sysreport.legacy
%{_datadir}/sos
%{_datadir}/sysreport
%{_mandir}/man1/sosreport.1*

%dir %{py_sitescriptdir}/sos
%dir %{py_sitescriptdir}/sos/plugins
%{py_sitescriptdir}/sos/*.py[co]
%{py_sitescriptdir}/sos/plugins/*.py[co]
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/sos-*.egg-info
%endif
