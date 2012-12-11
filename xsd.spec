Summary:	W3C XML schema to C++ data binding compiler
Name:		xsd
Version:	3.3.0
Release:	4
Group:		Development/C++
# Exceptions permit otherwise GPLv2 incompatible combination with ASL 2.0
License:	GPLv2 with exceptions and ASL 2.0
URL:		http://www.codesynthesis.com/products/xsd/
Source0:	http://www.codesynthesis.com/download/xsd/3.3/xsd-%{version}-2+dep.tar.bz2
# Suggestion sent to upstream via e-mail 20090707
Patch0:		xsd-3.3.0-xsdcxx-rename.patch

BuildRequires:	boost-devel
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

%package	doc
Group:		Books/Computer books
Summary:	API documentation files for %{name}

%description	doc
This package contains API documentation for %{name}.


%prep
%setup -q -n xsd-%{version}-2+dep
pushd xsd
%patch0 -p1 -b .xsdcxx-rename
popd

%build
make verbose=0 CXXFLAGS="%{optflags}"

%install
rm -rf apidocdir

%makeinstall_std install_prefix="%{buildroot}%{_prefix}"

# Split API documentation to -doc subpackage.
mkdir apidocdir
mv %{buildroot}%{_datadir}/doc/xsd/*.{xhtml,css} apidocdir/
mv %{buildroot}%{_datadir}/doc/xsd/cxx/ apidocdir/
mv %{buildroot}%{_datadir}/doc/xsd/ docdir/

# Convert to utf-8.
for file in docdir/NEWS; do
    mv $file timestamp
    iconv -f ISO-8859-1 -t UTF-8 -o $file timestamp
    touch -r timestamp $file
done

# Rename binary to xsdcxx to avoid conflicting with mono-web package.
# Sent suggestion to upstream via e-mail 20090707
# they will consider renaming in 4.0.0
mv %{buildroot}%{_bindir}/xsd %{buildroot}%{_bindir}/xsdcxx
mv %{buildroot}%{_mandir}/man1/xsd.1 %{buildroot}%{_mandir}/man1/xsdcxx.1

# Remove duplicate docs.
rm -rf %{buildroot}%{_datadir}/doc/libxsd

# Remove Microsoft Visual C++ compiler helper files.
rm -rf %{buildroot}%{_includedir}/xsd/cxx/compilers

# Remove redundant PostScript files that rpmlint grunts about not being UTF8
# See: https://bugzilla.redhat.com/show_bug.cgi?id=502024#c27
# for Boris Kolpackov's explanation about those
find apidocdir -name "*.ps" | xargs rm -f
# Remove other unwanted crap
find apidocdir -name "*.doxygen" \
            -o -name "makefile" \
            -o -name "*.html2ps" | xargs rm -f

%files
%doc docdir/*
%{_bindir}/xsdcxx
%{_mandir}/man1/xsdcxx.1*

%files devel
%{_includedir}/xsd/

%files doc
%doc apidocdir/*


