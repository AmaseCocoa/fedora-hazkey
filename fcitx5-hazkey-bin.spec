# Maintainer: AmaseCocoa <cocoa@amase.cc>
%global debug_package %{nil}
%define _build_id_links none

Name:           fcitx5-hazkey-bin
Version:        0.2.1
Release:        2%{?dist}
Summary:        Binary distribution for fcitx5-hazkey

License:        MIT
URL:            https://hazkey.hiira.dev/
Source0:        https://github.com/7ka-Hiira/fcitx5-hazkey/releases/download/%{version}/fcitx5-hazkey-%{version}-x86_64.tar.gz
Source1:        https://raw.githubusercontent.com/7ka-Hiira/hazkey/refs/tags/0.2.1/LICENSE

BuildRequires:  tar
Requires:       fcitx5
Requires:       qt6-qtbase
Requires:       vulkan-loader
Requires:       glibc
Requires:       gcc-c++

Conflicts:      fcitx5-hazkey
Provides:       fcitx5-hazkey = %{version}
Provides:       hazkey-server
Provides:       hazkey-settings

%description
Japanese input method for fcitx5, powered by azooKey engine

%prep
%setup -q -c -n fcitx5-hazkey-%{version}

%build

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/fcitx5
mkdir -p %{buildroot}%{_libdir}/hazkey
mkdir -p %{buildroot}%{_datadir}

cp -a usr/bin/* %{buildroot}%{_bindir}/
cp -a usr/bin/* %{buildroot}%{_bindir}/
cp -a usr/lib/x86_64-linux-gnu/* %{buildroot}%{_libdir}/

cp -a usr/share/* %{buildroot}%{_datadir}/

rm -f %{buildroot}%{_bindir}/hazkey-settings
ln -s ../%{_lib}/hazkey/hazkey-settings %{buildroot}%{_bindir}/hazkey-settings

sed -i 's|/usr/lib/x86_64-linux-gnu/hazkey|%{_libdir}/hazkey|g' %{buildroot}%{_bindir}/hazkey-server
sed -i 's|x86_64-linux-gnu/||g' %{buildroot}%{_bindir}/hazkey-server

sed -i '/# hazkey-server wrapper script/a \
if [ -z "${GGML_BACKEND_DIR}" ] ; then \
    export GGML_BACKEND_DIR=%{_libdir}/hazkey/libllama/backends/ \
fi' %{buildroot}%{_bindir}/hazkey-server

mkdir -p %{buildroot}%{_datadir}/licenses/%{name}
install -Dpm 644 %{SOURCE1} %{buildroot}%{_datadir}/licenses/%{name}/LICENSE

%files
%{_bindir}/hazkey-server
%{_bindir}/hazkey-settings
%{_libdir}/fcitx5/
%{_libdir}/hazkey/
%{_datadir}/applications/*.desktop
%{_datadir}/fcitx5/
%{_datadir}/hazkey/
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/locale/ja/LC_MESSAGES/*.mo
%{_datadir}/metainfo/*.xml
%{_datadir}/licenses/%{name}/LICENSE

%changelog
* Wed Feb 11 2026 AmaseCocoa <cocoa@amase.cc> - 0.2.1-2
- fcitx5-hazkey Fedora binary package.
