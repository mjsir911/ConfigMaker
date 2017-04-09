PYTH = python2.7
VENV = venv


.PHONY: all build clean

all: requirements

build: $(VENV)/bin/py2applet setup.py
	#$(VENV)/bin/py2applet -s -d build/ src/makeconf.py
	$(VENV)/bin/$(PYTH) setup.py py2app
	@rm -rf "build/makeconf-$(shell date -u +"%Y-%m-%d").app"
	mv build/makeconf.app "build/makeconf-$(shell date -u +"%Y-%m-%d").app"
	rm -rf build/bdist*

setup.py: $(VENV)/bin/py2applet
	venv/bin/py2applet --make-setup -a -s --site-packages --packages=PySide -d build/ src/makeconf.py

$(VENV)/bin/py2applet: requirements

requirements: $(VENV)

$(VENV): venv/bin/activate requirements.txt
	$(VENV)/bin/pip install -U pip
	$(VENV)/bin/pip install -Ur requirements.txt
	$(VENV)/bin/pyside_postinstall.py -install # dont think needed but ok

$(VENV)/bin/activate: 
	virtualenv $(VENV) --python=$(PYTH)
