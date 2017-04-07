#!/bin/bash
#
# install.sh
# Written by Kevin Cole <kevin.cole@novawebcoop.org> 2017.04.02
#
# This determines if we're in a Python virtual environment, and,
# if so, creates a Mac OS X ".app"
#
# Note: This installer was designed with and for Mac OS X 10.12.4
# (Sierra).  py2app in particular, is used to "bundle" the python code
# into Mac apps and "brand" them with an icon I designed.
#

if [ -z ${VIRTUAL_ENV} ]
then
  echo "You must run this from a Python virtual environment."
  echo "(Read up on virtualenv for more info.)"
else
  git checkout stable
  git fetch upstream
  git merge upstream/stable
  git push
  git pull
  rm -rf build dist
  rm setup.py
  py2applet --make-setup src/makeconf.py
  perl -p -i -e "s|True|False|g;" setup.py
  python2.7 setup.py py2app -A
  rm setup.py
fi
