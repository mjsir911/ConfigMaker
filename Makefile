PYTH = python2.7
VENV = venv
BUILD = build# probs not best practice
APP = $(BUILD)/makeconf.app/
SRC = src



.PHONY: all build clean

#$(VENV)/bin/py2applet -s -d build/ src/makeconf.py
#rm -rf $(BUILD)/bdist*
#"build/makeconf-$(shell date -u +"%Y-%m-%d").app"
all: venv build

build: $(APP)

$(APP): $(VENV)/bin/py2applet setup.py $(SRC)/makeconf.py
	$(VENV)/bin/$(PYTH) setup.py py2app

#makeconf depends on contents
$(SRC)/makeconf.py: $(SRC)/contents.py
	@touch $(SRC)/makeconf.py

setup.py: $(VENV)/bin/py2applet
	rm -f setup.py
	venv/bin/py2applet --make-setup -a -s --site-packages --packages=PySide -d $(BUILD) -b $(BUILD) $(SRC)/makeconf.py

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
