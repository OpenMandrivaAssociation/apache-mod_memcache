#Module-Specific definitions
%define apache_version 2.2.4
%define mod_name mod_memcache
%define mod_conf B10_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DSO module for the apache Web server
Name:		apache-%{mod_name}
Version:	0.1.0
Release:	%mkrel 4
Group:		System/Servers
License:	Apache License
URL:		http://code.google.com/p/modmemcache/
Source0:	http://modmemcache.googlecode.com/files/mod_memcache-%{version}.tar.gz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= %{apache_version}
Requires(pre):  apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:  apache-devel >= %{apache_version}
BuildRequires:  apr_memcache-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
mod_memcache manages the parsing of memcached server configuration and exports
a single function for use by other modules to access a configured apr_memcache
object.

%prep

%setup -q -n %{mod_name}-%{version}

cp %{SOURCE1} %{mod_conf}

%build
export CPPFLAGS="-I%{_includedir}/apr_memcache-0"

%configure2_5x \
    --with-apr-memcache=%{_prefix} \
    --with-apxs=%{_sbindir}/apxs

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std AP_LIBEXECDIR=%{_libdir}/apache-extramodules

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/mod_memcache.so
%attr(0755,root,root) %{_libdir}/apache-extramodules/mod_memcache_example.so
