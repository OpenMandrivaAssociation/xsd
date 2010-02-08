%define version 3.2.0
%define rel 5
%define release %mkrel %rel

Name:		xsd
Version:        %{version}
Release:        %{release}
Summary:        W3C XML schema to C++ data binding compiler

Group:          Development/C++
# Exceptions permit otherwise GPLv2 incompatible combination with ASL 2.0
License:        GPLv2 with exceptions and ASL 2.0  
URL:            http://www.codesynthesis.com/products/xsd/
Source0:        http://www.codesynthesis.com/download/xsd/3.2/xsd-%{version}+dep.tar.bz2
Patch0:         xsd-3.2.0-xsdcxx-rename.patch
Patch1:         xsd-3.2.0-manfix.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  boost-devel
BuildRequires:	xerces-c-devel
BuildRequires:	m4
# Requires:  ace-devel - only needed for applications using
#                        Adaptive Communication Environment (ACE) streams,
#                        enable when Fedora gets ACE packages.
#                        See http://www.cs.wustl.edu/~schmidt/ACE.html and
#                        https://bugzilla.redhat.com/show_bug.cgi?id=450164

%description
CodeSynthesis XSD is an open-source, cross-platform W3C XML Schema to
C++ data binding compiler. Provided with an XML instance specification
(XML Schema), it generates C++ classes that represent the given
vocabulary as well as parsing and serialization code.
You can then access the data stored in XML using types and functions
that semantically correspond to your application domain rather than
dealing with intricacies of reading and writing XML.


%package	devel
Group:		System/Libraries
Summary:	Development files for xsd
Requires:	xerces-c-devel
Requires:	%{name} = %{version}

%description	devel
This package provides development files for xsd.

%package        doc
Group:          Books/Computer books
Summary:        API documentation files for %{name}

%description    doc
This package contains API documentation for %{name}.


%prep
%setup -q -n xsd-%{version}+dep
pushd xsd-*
%patch0 -p1 -b .xsdcxx-rename
%patch1 -p1 -b .manfix
popd


%build
MAKEFLAGS="verbose=1" CXXFLAGS=$RPM_OPT_FLAGS ./build.sh


%install
rm -rf $RPM_BUILD_ROOT
rm -rf apidocdir

MAKEFLAGS="install_prefix=$RPM_BUILD_ROOT%{_prefix}" ./build.sh install

# Split API documentation to -doc subpackage.
mkdir apidocdir
mv $RPM_BUILD_ROOT%{_datadir}/doc/xsd/*.{xhtml,css} apidocdir/
mv $RPM_BUILD_ROOT%{_datadir}/doc/xsd/cxx/ apidocdir/
mv $RPM_BUILD_ROOT%{_datadir}/doc/xsd/ docdir/

# Convert to utf-8.
for file in docdir/NEWS; do
    mv $file timestamp
    iconv -f ISO-8859-1 -t UTF-8 -o $file timestamp
    touch -r timestamp $file
done

# Rename binary to xsdcxx to avoid conflicting with mono-web package.
mv $RPM_BUILD_ROOT%{_bindir}/xsd $RPM_BUILD_ROOT%{_bindir}/xsdcxx
mv $RPM_BUILD_ROOT%{_mandir}/man1/xsd.1 $RPM_BUILD_ROOT%{_mandir}/man1/xsdcxx.1

# Remove duplicate docs.
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/libxsd

# Remove Microsoft Visual C++ compiler helper files.
rm -rf $RPM_BUILD_ROOT%{_includedir}/xsd/cxx/compilers

# Remove redundant PostScript files that rpmlint grunts about not being UTF8
# See: https://bugzilla.redhat.com/show_bug.cgi?id=502024#c27
# for Boris Kolpackov's explanation about those
find apidocdir -name "*.ps" | xargs rm -f
# Remove other unwanted crap
find apidocdir -name "*.doxygen" \
            -o -name "makefile" \
            -o -name "*.html2ps" | xargs rm -f

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc docdir/*
%{_bindir}/xsdcxx
%{_mandir}/man1/xsdcxx.1*

%files devel
%defattr(-,root,root,-)
%{_includedir}/xsd/

%files doc
%defattr(-,root,root,-)
%doc apidocdir/*


