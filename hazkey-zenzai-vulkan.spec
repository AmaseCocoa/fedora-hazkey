# Maintainer: AmaseCocoa <cocoa@amase.cc>

%define _llamacpp_ver 20251109.0

Name:           hazkey-zenzai-vulkan
Version:        0.2.0
Release:        2%{?dist}
Summary:        Zenzai neural conversion module for Hazkey (Vulkan Backend)
License:        MIT
URL:            https://github.com/7ka-Hiira/fcitx5-hazkey
Source0:        https://github.com/7ka-Hiira/llama.cpp/archive/refs/tags/v%{_llamacpp_ver}.tar.gz
Source1:        https://huggingface.co/Miwa-Keita/zenz-v3.1-small-gguf/resolve/main/ggml-model-Q5_K_M.gguf

BuildRequires:  cmake >= 3.21
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
BuildRequires:  vulkan-headers
BuildRequires:  vulkan-loader-devel
BuildRequires:  shaderc-devel

Requires:       hazkey-server
Requires:       vulkan-loader
Provides:       hazkey-zenzai = %{version}-%{release}

%description
Zenzai neural conversion module for Hazkey.
This version is built with Vulkan support for GPU acceleration.

%prep
%setup -q -n llama.cpp-%{_llamacpp_ver}

%build
%cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_RPATH='$ORIGIN' \
    -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON \
    -DCMAKE_SKIP_BUILD_RPATH=ON \
    -DBUILD_SHARED_LIBS=ON \
    -DLLAMA_CURL=OFF \
    -DLLAMA_STANDALONE=OFF \
    -DLLAMA_BUILD_TESTS=OFF \
    -DLLAMA_BUILD_EXAMPLES=OFF \
    -DLLAMA_BUILD_SERVER=OFF \
    -DLLAMA_ALL_WARNINGS=OFF \
    -DLLAMA_FATAL_WARNINGS=OFF \
    -DLLAMA_LLGUIDANCE=OFF \
    -DGGML_RPC=OFF \
    -DGGML_SCHED_MAX_COPIES=2 \
    -DGGML_NATIVE=ON \
    -DGGML_LTO=ON \
    -DGGML_VULKAN=ON

%cmake_build

%install
mkdir -p %{buildroot}%{_libdir}/hazkey/llama
pushd %{_vpath_builddir}/bin
install -m 755 libggml.so %{buildroot}%{_libdir}/hazkey/llama/
install -m 755 libggml-base.so %{buildroot}%{_libdir}/hazkey/llama/
install -m 755 libggml-vulkan.so %{buildroot}%{_libdir}/hazkey/llama/
install -m 755 libggml-cpu.so %{buildroot}%{_libdir}/hazkey/llama/
install -m 755 libllama.so %{buildroot}%{_libdir}/hazkey/llama/
popd

install -Dm 644 %{SOURCE1} %{buildroot}%{_datadir}/hazkey/zenzai.gguf

install -Dm 644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE

%files
%{_libdir}/hazkey/llama/*.so
%{_datadir}/hazkey/zenzai.gguf
%{_datadir}/licenses/%{name}/LICENSE

%changelog
* Wed Feb 11 2026 AmaseCocoa <cocoa@amase.cc> - 0.2.0-2
- Ported from PKGBUILD
- Enabled Vulkan backend for GGML
- Added Zenzai model GGUF file
