# Maintainer: AmaseCocoa <cocoa@amase.cc>

%define _dictionaryversion 3.0.1
%define _emojiversion 08f82252fb90ef8f0949a7e3c554e9e1787ce121
%define _llamaversion 10295c26a2a18c3c48863b179c5e6bf34a4057d1

Name:           fcitx5-hazkey
Version:        0.2.1
Release:        2%{?dist}
Summary:        Japanese input method for fcitx5, powered by azooKey engine
License:        MIT
URL:            https://hazkey.hiira.dev/
Source0:        https://github.com/7ka-Hiira/fcitx5-hazkey/archive/refs/tags/%{version}.tar.gz
Source1:        https://github.com/7ka-Hiira/llama.cpp/archive/%{_llamaversion}.zip
Source2:        https://github.com/azooKey/azooKey_dictionary_storage/archive/refs/tags/v%{_dictionaryversion}.zip
Source3:        https://github.com/azooKey/azooKey_emoji_dictionary_storage/archive/%{_emojiversion}.zip

BuildRequires:  swift-lang >= 6.1
BuildRequires:  cmake >= 3.21
BuildRequires:  ninja-build
BuildRequires:  fcitx5-devel >= 5.0.4
BuildRequires:  qt6-qtbase-devel >= 6.7
BuildRequires:  protobuf-devel
BuildRequires:  vulkan-headers
BuildRequires:  libshaderc-devel
BuildRequires:  gettext
BuildRequires:  findutils, sed

Requires:       fcitx5 >= 5.0.4
Requires:       qt6-qtbase
Provides:       hazkey-server = %{version}
Provides:       hazkey-settings = %{version}

%description
Hazkey is a Japanese input method for fcitx5.
This package is built with an automated workaround for Swift 6.1 header conflicts.

%prep
%setup -q -n fcitx5-hazkey-%{version}

unzip -q %{SOURCE1}
unzip -q %{SOURCE2}
unzip -q %{SOURCE3}

rm -rf hazkey-server/llama.cpp
mv llama.cpp-%{_llamaversion} hazkey-server/llama.cpp

cp -r azooKey_dictionary_storage-%{_dictionaryversion}/Dictionary hazkey-server/azooKey_dictionary_storage/
cp -r azooKey_emoji_dictionary_storage-%{_emojiversion}/EmojiDictionary hazkey-server/azooKey_emoji_dictionary_storage/

%build
ORIGINAL_HEADER=$(find %{_libdir}/swift* -name "_CStdlib.h" | grep "_FoundationCShims" | head -n 1)
mkdir -p %{_vpath_builddir}/shim_fixes/_FoundationCShims
cp "$ORIGINAL_HEADER" %{_vpath_builddir}/shim_fixes/_FoundationCShims/_CStdlib.h
sed -i '/#if __has_include(<math.h>)/,/#endif/ s/^/\/\//' %{_vpath_builddir}/shim_fixes/_FoundationCShims/_CStdlib.h

%cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_Swift_FLAGS="-Xcc -I%{_builddir}/fcitx5-hazkey-%{version}/%{_vpath_builddir}/shim_fixes" \
    -DGGML_VULKAN=ON

%cmake_build

%install
%cmake_install

install -Dm644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE

%files
%{_libdir}/fcitx5/
%{_datadir}/fcitx5/
%{_datadir}/licenses/%{name}/LICENSE
%{_datadir}/locale/*/LC_MESSAGES/*.mo

%changelog
* Wed Feb 11 2026 AmaseCocoa <cocoa@amase.cc> - 0.2.1
- Ported from PKGBUILD 0.2.1-2
- Integrated automated patch for Swift 6.1 math.h redefinition issue
- Bundle dictionary and llama.cpp sources as per upstream requirements
