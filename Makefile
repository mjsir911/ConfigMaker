PYTH = python2.7
VENV = venv
BUILD = build/# probs not best practice
APP = $(BUILD)/makeconf.app


.PHONY: all build clean

#$(VENV)/bin/py2applet -s -d build/ src/makeconf.py
all: venv build

build: $(APP)

$(APP): $(VENV)/bin/py2applet setup.py src/makeconf.py src/contents.py
	echo $(APP)
	$(VENV)/bin/$(PYTH) setup.py py2app
	@rm -rf "build/makeconf-$(shell date -u +"%Y-%m-%d").app"
	#mv build/makeconf.app "build/makeconf-$(shell date -u +"%Y-%m-%d").app"
	rm -rf build/bdist*

setup.py: $(VENV)/bin/py2applet
	rm -f setup.py
	venv/bin/py2applet --make-setup -a -s --site-packages --packages=PySide -d $(BUILD) -b $(BUILD) src/makeconf.py

$(VENV)/bin/py2applet: requirements

requirements: pip

pip: $(VENV)/pip-selfcheck.json 

$(VENV)/pip-selfcheck.json: $(VENV) requirements.txt
	$(VENV)/bin/pip install -U pip
	$(VENV)/bin/pip install -Ur requirements.txt
	$(VENV)/bin/pyside_postinstall.py -install # dont think needed but ok
	touch $(VENV)/pip-selfcheck.json

$(VENV):
	virtualenv $(VENV) --python=$(PYTH)
	rm -f $(VENV)/pip-selfcheck.json
