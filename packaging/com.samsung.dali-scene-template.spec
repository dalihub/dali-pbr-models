%bcond_with wayland

Name:       com.samsung.dali-scene-template
Summary:    Scenes for DALi demo.
Version:    1.0.0
Release:    1
Group:      Scenes for DALi demo
License:    Apache-2.0
URL:        https://github.com/dalihub/dali-scene-template
Source0:    %{name}-%{version}.tar.gz

BuildRequires:  cmake

#need libtzplatform-config for directory if tizen version is 3.x
BuildRequires:  pkgconfig(libtzplatform-config)

%description
Scenes for DALi demo

##############################
# Preparation
##############################
%prep
%setup -q

#Use TZ_PATH when tizen version is 3.x
%define dali_app_ro_dir       %TZ_SYS_RO_APP/com.samsung.dali-demo

%define smack_rule_dir        %TZ_SYS_SMACK/accesses2.d/

##############################
# Build
##############################
%build

cd %{_builddir}/%{name}-%{version}/build/tizen

cmake -DDALI_APP_RES_DIR=%{dali_app_ro_dir}

##############################
# Installation
##############################
%install
rm -rf %{buildroot}
cd build/tizen
%make_install DALI_APP_RES_DIR=%{dali_app_ro_dir}

%if 0%{?enable_dali_smack_rules} && !%{with wayland}
mkdir -p %{buildroot}%{smack_rule_dir}
cp -f %{_builddir}/%{name}-%{version}/%{name}.rule %{buildroot}%{smack_rule_dir}
%endif

##############################
# Files in Binary Packages
##############################

%files
%if 0%{?enable_dali_smack_rules}
%manifest %{name}.manifest-smack
%else
%manifest %{name}.manifest
%endif
%defattr(-,root,root,-)
%{dali_app_ro_dir}/images/scenes/*
%{dali_app_ro_dir}/models/scenes/*
%{dali_app_ro_dir}/shaders/scenes/*
%license LICENSE
%if 0%{?enable_dali_smack_rules} && !%{with wayland}
%config %{smack_rule_dir}/%{name}.rule
%endif