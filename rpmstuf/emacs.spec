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
#### Afadli
Source1:       emacs.desktop
Source2:       dotemacs.el
Source3:       site-start.el
Source4:       default.el
# Emacs Terminal Mode, #551949, #617355
Source5:       emacs-terminal.desktop
Source6:       emacs-terminal.sh
Source7:       emacs.service
Source8:      %{name}.appdata.xml
# rhbz#713600
Patch1:        emacs-spellchecker.patch
Patch2:        emacs-system-crypto-policies.patch

BuildRequires: gcc
BuildRequires: atk-devel
BuildRequires: cairo-devel
BuildRequires: freetype-devel
BuildRequires: fontconfig-devel
BuildRequires: dbus-devel
BuildRequires: giflib-devel
BuildRequires: glibc-devel
BuildRequires: libpng-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: libjpeg-turbo
BuildRequires: libtiff-devel
BuildRequires: libX11-devel
BuildRequires: libXau-devel
BuildRequires: libXdmcp-devel
BuildRequires: libXrender-devel
BuildRequires: libXt-devel
BuildRequires: libXpm-devel
BuildRequires: ncurses-devel
BuildRequires: xorg-x11-proto-devel
BuildRequires: zlib-devel
BuildRequires: gnutls-devel
BuildRequires: librsvg2-devel
BuildRequires: m17n-lib
BuildRequires: libotf
BuildRequires: libselinux-devel
BuildRequires: alsa-lib-devel
BuildRequires: gpm-devel
BuildRequires: liblockfile-devel
BuildRequires: libxml2-devel
BuildRequires: autoconf
BuildRequires: bzip2
BuildRequires: cairo
BuildRequires: texinfo
BuildRequires: gzip
BuildRequires: desktop-file-utils
BuildRequires: libacl-devel
BuildRequires: harfbuzz-devel
BuildRequires: jansson-devel
BuildRequires: systemd-devel

BuildRequires: gtk3-devel
BuildRequires: webkit2gtk3-devel


#Requires:
Obsoletes:      emacs

#######

# Emacs doesn't run without dejavu-sans-mono-fonts, rhbz#732422
Requires:      desktop-file-utils
Requires:      dejavu-sans-mono-fonts
Requires(preun): %{_sbindir}/alternatives
Requires(posttrans): %{_sbindir}/alternatives
Requires:      emacs-common = %{epoch}:%{version}-%{release}
Provides:      emacs(bin) = %{epoch}:%{version}-%{release}

%define site_lisp %{_datadir}/emacs/site-lisp
%define site_start_d %{site_lisp}/site-start.d
%define bytecompargs -batch --no-init-file --no-site-file -f batch-byte-compile
%define pkgconfig %{_datadir}/pkgconfig
%define emacs_libexecdir %{_libexecdir}/emacs/%{version}/%{_host}

########

%description
Latest GNU Emacs
Emacs is a powerful, customizable, self-documenting, modeless text
editor. Emacs contains special code editing features, a scripting
language (elisp), and the capability to read mail, news, and more
without leaving the editor.

########Afadli
%prep
[ -f %{SOURCE0} ] || curl -L http://mirrors.ustc.edu.cn/gnu/emacs/emacs-%{version}.tar.gz -o %{SOURCE0}
tar xzf %{SOURCE0} --strip-components=1

%setup -q

%patch1 -p1 -b .spellchecker
%patch2 -p1 -b .system-crypto-policies
autoconf

# We prefer our emacs.desktop file
cp %SOURCE1 etc/emacs.desktop


grep -v "tetris.elc" lisp/Makefile.in > lisp/Makefile.in.new \
   && mv lisp/Makefile.in.new lisp/Makefile.in
grep -v "pong.elc" lisp/Makefile.in > lisp/Makefile.in.new \
   && mv lisp/Makefile.in.new lisp/Makefile.in

# Avoid trademark issues
rm -f lisp/play/tetris.el lisp/play/tetris.elc
rm -f lisp/play/pong.el lisp/play/pong.el


# Sorted list of info files
%define info_files ada-mode auth autotype bovine calc ccmode cl dbus dired-x ebrowse ede ediff edt efaq-w32 efaq eieio eintr elisp emacs-gnutls emacs-mime emacs epa erc ert eshell eudc eww flymake forms gnus htmlfontify idlwave ido info mairix-el message mh-e newsticker nxml-mode octave-mode org pcl-cvs pgg rcirc reftex remember sasl sc semantic ses sieve smtpmail speedbar srecode todo-mode tramp url vhdl-mode vip viper widget wisent woman

# Since the list of info files has to be maintained, check if all info files
# from the upstream tarball are actually present in %%info_files.
cd info
fs=( $(ls *.info) )
is=( %info_files  )
files=$(echo ${fs[*]} | sed 's/\.info//'g | sort | tr -d '\n')
for i in $(seq 0 $(( ${#fs[*]} - 1 ))); do
  if test "${fs[$i]}" != "${is[$i]}.info"; then
    echo Please update %%info_files: ${fs[$i]} != ${is[$i]}.info >&2
    break
  fi
done
cd ..

%ifarch %{ix86}
%define setarch setarch %{_arch} -R
%else
%define setarch %{nil}
%endif


#####



%build
export CFLAGS="-DMAIL_USE_LOCKF %{build_cflags}"
# Build GTK+ binary
mkdir build-gtk && cd build-gtk
ln -s ../configure .

LDFLAGS=-Wl,-z,relro;  export LDFLAGS;

%configure --with-dbus --with-gif --with-jpeg --with-png --with-rsvg \
           --with-tiff --with-xft --with-xpm --with-x-toolkit=gtk3 --with-gpm=no \
           --with-xwidgets --with-modules --with-harfbuzz --with-cairo --with-json --with-pop --with-mailutils
make %{?_smp_mflags}


# Create pkgconfig file
cat > emacs.pc << EOF
sitepkglispdir=%{site_lisp}
sitestartdir=%{site_start_d}

Name: emacs
Description: GNU Emacs text editor
Version: %{epoch}:%{version}
EOF

# Create macros.emacs RPM macro file
cat > macros.emacs << EOF
%%_emacs_version %{version}
%%_emacs_ev %{?epoch:%{epoch}:}%{version}
%%_emacs_evr %{?epoch:%{epoch}:}%{version}-%{release}
%%_emacs_sitelispdir %{site_lisp}
%%_emacs_sitestartdir %{site_start_d}
%%_emacs_bytecompile /usr/bin/emacs -batch --no-init-file --no-site-file --eval '(progn (setq load-path (cons "." load-path)))' -f batch-byte-compile
EOF

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
