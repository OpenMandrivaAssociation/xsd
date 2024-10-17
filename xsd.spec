%define _disable_lto 1
%define _disable_ld_no_undefined 1

# NOTE: this package use bundled libcutl

Summary:	W3C XML schema to C++ data binding compiler
Name:		xsd
Version:	4.1.0
Release:	4
Group:		Development/C++
# Exceptions permit otherwise GPLv2 incompatible combination with ASL 2.0
License:	GPLv2 with exceptions and ASL 2.0
URL:		https://www.codesynthesis.com/products/xsd/
Source0:	https://codesynthesis.com/~boris/tmp/xsd/%{version}.a11/xsd-%{version}.a11+dep.tar.bz2
# (fedora)  Suggestion sent to upstream via e-mail 20090707
Patch0:		xsd-4.1.0-xsdcxx-rename.patch

# (fedora) Remove tests for character reference values unsupported by Xerces-C++ 3.2
# https://anonscm.debian.org/cgit/collab-maint/xsd.git/diff/debian/patches/0110-xerces-c3.2.patch?id=442e98604d4158dae11056c4f94aaa655cb480fa
Patch1: %{name}-xerces_3-2.patch

BuildRequires:	boost-devel
BuildRequires:	pkgconfig(xerces-c)
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

%files
%doc docdir/*
%{_bindir}/xsdcxx
%{_mandir}/man1/xsdcxx.1*

#---------------------------------------------------------------------------

%package	devel
Summary:	Development files for xsd
Group:		System/Libraries
Requires:	xerces-c-devel
Requires:	%{name} = %{version}

%description	devel
This package provides development files for xsd.

%files devel
%{_includedir}/xsd/

#---------------------------------------------------------------------------

%package	doc
Summary:	API documentation files for %{name}
Group:		Books/Computer books
BuildRequires:	ghostscript
%description	doc
This package contains API documentation for %{name}.

%files doc
%doc apidocdir/*

#---------------------------------------------------------------------------

%prep
%autosetup -p0 -n xsd-%{version}.a11+dep

%build
%make_build \
	verbose=1 \
	CXX=g++ \
	CC=gcc \
	CXXFLAGS="%{optflags} -std=c++14 -fPIC -pie -Wl,-z,now" 	\
	LDFLAGS="%{__global_ldflags} -fPIC -pie -Wl,-z,now"	\
	BOOST_LINK_SYSTEM=y


%install
rm -rf apidocdir

%make_install \
	LDFLAGS="%{__global_ldflags}" \
	install_prefix=%{buildroot}%{_prefix} \
	install_bin_dir=%{buildroot}%{_bindir} \
	install_man_dir=%{buildroot}%{_mandir} \
	BOOST_LINK_SYSTEM=y


# Split API documentation to -doc subpackage.
mkdir -p apidocdir
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
