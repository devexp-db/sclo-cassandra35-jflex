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

Summary:        Fast Scanner Generator
Name:           jflex
Version:        1.4.3
Release:        9%{?dist}
Epoch:          0
License:        GPL+
URL:            http://jflex.de/
Group:          Development/Libraries
Source0:        http://jflex.de/%{name}-%{version}.tar.gz
Source1:        http://repo2.maven.org/maven2/de/jflex/jflex/1.4.3/jflex-1.4.3.pom
Source2:        %{name}.desktop
Source3:        %{name}.png

Patch0:         jflex-build_xml.patch
Patch1:         jflex-junit-incompatibility.patch

BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:  ant
BuildRequires:  junit
BuildRequires:  java-devel
BuildRequires:  java_cup
BuildRequires:  desktop-file-utils
Requires:       java
Requires:       java_cup
BuildArch:      noarch

%description
JFlex is a lexical analyzer generator (also known as scanner
generator) for Java(tm), written in Java(tm). It is also a
rewrite of the very useful tool JLex which was developed by
Elliot Berk at Princeton University. As Vern Paxson states
for his C/C++ tool flex: They do not share any code though.
JFlex is designed to work together with the LALR parser
generator CUP by Scott Hudson, and the Java modification of
Berkeley Yacc BYacc/J by Bob Jamison. It can also be used
together with other parser generators like ANTLR or as a
standalone tool.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation

%description javadoc
%{summary}.

%prep
%setup -q
%patch0 -b .sav
%patch1 -p1 -b .sav

for j in $(find . -name "*.jar"); do mv $j $j.no; done
find . -name "*.class" -exec rm {} \;

%{__sed} -i 's/\r//' COPYRIGHT
%{__sed} -i 's|includes="JFlex/\*\*,java_cup/\*\*,skeleton|includes="JFlex/\*\*,skeleton|g' src/build.xml

%build

pushd src
# intial build using the autogenerated sym.java LexParse.java and LexScan.java
# these are created by the jflex ant task which needs to be built first
CLASSPATH=%{_javadir}/junit.jar:%{_javadir}/java_cup.jar ant jar-bootstrap
# now that the JFlex.jar has been build we can use jflex ant tasks
# removing the generated files and rebuilding using the JFlex.jar
CLASSPATH=%{_javadir}/junit.jar:%{_javadir}/java_cup.jar:../lib/JFlex.jar ant genclean libclean jar

javadoc -sourcepath . -d ../api JFlex
popd

%install

# jars
mkdir -p %{buildroot}%{_javadir}
cp -p lib/JFlex.jar %{buildroot}%{_javadir}/%{name}.jar
(cd %{buildroot}%{_javadir} && ln -sf %{name}.jar JFlex.jar)

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 %{SOURCE1} %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap JPP-%{name}.pom %{name}.jar

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -pr api/* %{buildroot}%{_javadocdir}/%{name}

# docs
mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
cp -p doc/* %{buildroot}%{_docdir}/%{name}-%{version}
cp -p COPYRIGHT %{buildroot}%{_docdir}/%{name}-%{version}

# wrapper script for direct execution
%jpackage_script JFlex.Main "" "" jflex:java_cup jflex true

# .desktop + icons
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE2}
install -Dpm 644 %{SOURCE3} %{buildroot}%{_datadir}/pixmaps/%{name}.png

%pre javadoc
# workaround for rpm bug, can be removed in F-21
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :

%files
%doc %{_docdir}/%{name}-%{version}
%{_javadir}/%{name}.jar
%{_javadir}/JFlex.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png

%files javadoc
%doc %{_javadocdir}/%{name}


%changelog
* Wed May  2 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.4.3-9
- Fix license tag

* Thu Apr 19 2012 Jaromir Capik <jcapik@redhat.com> - 0:1.4.3-8
- Desktop file generated
- Icon created from the GPL licensed logo

* Mon Mar 12 2012 Jaromir Capik <jcapik@redhat.com> - 0:1.4.3-7
- Wrapper script generated
- Minor spec file changes according to the latest guidelines

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 15 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.4.3-4
- Add dependency on java_cup in the maven pom.xml.

* Mon Feb 15 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.4.3-3
- Require java_cup.

* Wed Jan 20 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.4.3-3
- Provide JFlex.jar.
- Don't put java_cup classes in the jar.

* Fri Jan 8 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.4.3-2
- Add maven pom and depmaps.

* Fri Jan 8 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.4.3-1
- Update to 1.4.3.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4.1-0.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4.1-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.4.1-0.3
- drop repotag

* Mon Mar 03 2008 Matt Wringe <mwringe@redhat.com> - 0:1.4.1-0jpp.2
- Add missing buildrequires on java_cup

* Fri Feb 22 2008 Matt Wringe <mwringe@redhat.com> - 0:1.4.1-0jpp.1
- Patch build file to allow bootstrap building

* Mon Feb 18 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0:1.4.1-0jpp.1
- Naive attempt to update to newer version

* Mon Apr 02 2007 Matt Wringe <mwringe@redhat.com> - 0:1.3.5-2jpp.2
- Add patches jflex-CharSet_java.patch and jflex-StateSet_java.patch
  to allow building with the new gcj

* Mon Feb 12 2007 Matt Wringe <mwringe@redhat.com> - 0:1.3.5-2jpp.1
- Remove javadoc post and postun sections due to new jpp standard 
- Update makefile patch to compress jar
- Fix rpmlint issues

* Wed Jan 04 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.3.5-2jpp
- First JPP 1.7 build

* Wed Nov 16 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.3.5-1jpp
- First JPackage release
