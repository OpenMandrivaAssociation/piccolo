# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define _with_gcj_support 1
%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:
%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:
%{_gcj_support}}%{!?_gcj_support:0}}}

Summary:	Small fast XML parser
Name:		piccolo
Version:	1.04
Release:	2.2.10
License:	Apache Software License
Group:		Development/Java
Url:		http://piccolo.sourceforge.net/
Source0:	piccolo-%{version}-src.zip
Patch0:		piccolo-build_xml.patch
%if !%{gcj_support}
BuildArch:	noarch
%endif
%if %{gcj_support}
BuildRequires:	java-gcj-compat-devel
%endif
BuildRequires:	ant >= 0:1.6
BuildRequires:	ant-junit
BuildRequires:	java-rpmbuild >= 0:1.5.32
BuildRequires:	junit
Requires:	jpackage-utils

%description
Piccolo is a small, extremely fast XML parser for 
Java. It implements the SAX 1, SAX 2.0.1, and 
JAXP 1.1 (SAX parsing only) interfaces as a 
non-validating parser and attempts to detect 
all XML well-formedness errors. 

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description javadoc
%{summary}.

%prep
%setup -q -T -c -n %{name}-%{version}
cd ..
unzip -q %{SOURCE0}
cd %{name}-%{version}
rm -r src/org src/javax
%patch0
#Fix wrong-file-end-of-line-encoding
sed -i 's/\r$//g' LICENSE.txt

%build
export OPT_JAR_LIST="ant/ant-junit junit"
export CLASSPATH=
ant -Dbuild.sysclasspath=first build javadoc

%install
# jars
mkdir -p %{buildroot}%{_javadir}
cp -p lib/Piccolo.jar \
  %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -pr doc/javadoc/* %{buildroot}%{_javadocdir}/%{name}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%update_gcjdb

%postun
%clean_gcjdb
%endif

%files
%doc LICENSE.txt
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar

%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/piccolo-1.04.jar.*
%endif

%files javadoc
%doc %{_javadocdir}/*

