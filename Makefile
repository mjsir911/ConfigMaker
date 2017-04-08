PYTH = python2.7
VENV = venv
BUILD = $(date -u +"%Y-%m-%d")


.PHONY: all build clean

all: requirements

build: $(VENV)/bin/py2applet
	$(VENV)/bin/py2applet -s src/makeconf.py
	mv src/makeconf.app "build/makeconf-$(shell date -u +"%Y-%m-%d").app"

$(VENV)/bin/py2applet: requirements

requirements: $(VENV)

$(VENV): venv/bin/activate requirements.txt
	$(VENV)/bin/pip install -Ur requirements.txt

$(VENV)/bin/activate: 
	virtualenv $(VENV) --python=$(PYTH)
