# building emacs rpm from tarball

1. create .rpmmacro (check online for the macros)
2. run rpmdev-setuptree (it will create rpmbuid/{RPMS,SRPMS,...}
3. copy emacs.spec with this repo 
3.a you can get it by:
  1. yumdownlder --source <package>
  2. rpm2cpio <package>.src.rpm | cpio -civ '\*.spec'
  3. modify <package>.spec
4. run rpmbuild <poackage>.spec 
