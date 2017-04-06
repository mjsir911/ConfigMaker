#!/bin/bash
#
# install.sh
# Written by Kevin Cole <kevin.cole@novawebcoop.org> 2017.04.02
#
# This determines if we're in a Python virtual environment, and,
# if so, fetches and installs all the prerequisites.
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
  pip install -U pip
  pip install -r requirements.txt
  python2.7 $VIRTUAL_ENV/bin/pyside_postinstall.py -install
  cd src
  rm -rf build dist
  py2applet --make-setup makeconf.py
  python2.7 setup.py py2app -A
  rm setup.py
fi
