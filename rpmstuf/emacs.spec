Name:           emacs27
Version:        27.1
Release:        1%{?dist}
Summary:        GNU Emacs

#Group:
License:        GPL
URL:            http://www.gnu.org/software/emacs/
Source0:        http://mirrors.ustc.edu.cn/gnu/emacs/emacs-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ncurses-devel
#Requires:
Obsoletes:      emacs

%description
Latest GNU Emacs

%prep
[ -f %{SOURCE0} ] || curl -L http://mirrors.ustc.edu.cn/gnu/emacs/emacs-%{version}.tar.gz -o %{SOURCE0}
tar xzf %{SOURCE0} --strip-components=1

%build
%configure --with-dbus --with-gif --with-jpeg --with-png --with-rsvg \
           --with-tiff --with-xft --with-xpm --with-x-toolkit=gtk3 --with-gpm=no \
           --with-xwidgets --with-modules --with-harfbuzz --with-cairo --with-json
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find %{buildroot} -name ctags* -exec rm -f {} \;
rm -f %{buildroot}%{_infodir}/dir
mv %{buildroot}%{_infodir}/{info.info.gz,info.gz}

%clean
# rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_datadir}/applications/emacs.desktop
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/icons/hicolor/*/apps/emacs.png
%{_datadir}/icons/hicolor/scalable/apps/emacs.svg
%{_datadir}/icons/hicolor/scalable/apps/emacs.ico
%{_datadir}/icons/hicolor/scalable/mimetypes/emacs-document.svg
%doc
%{_bindir}/*
%{_mandir}/*/*
%{_infodir}/*
/usr/libexec/emacs
##/usr/share/appdata/emacs.appdata.xml
##/usr/share/applications/emacs.desktop
#/usr/share/emacs
#/usr/share/icons/hicolor/*/apps/*
#/usr/share/icons/hicolor/scalable/mimetypes/emacs-document*.svg
#/var/games/emacs

%changelog
