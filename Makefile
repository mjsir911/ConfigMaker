PYTH = python2.7
VENV = venv
BUILD = build
APP = ratings.app presets.app
SRC = src



.PHONY: all build clean $(APP)

#$(VENV)/bin/py2applet -s -d build/ src/makeconf.py
#rm -rf $(BUILD)/bdist*
#"build/makeconf-$(shell date -u +"%Y-%m-%d").app"
all: venv build

build: $(APP)

$(APP): % : $(BUILD)/%

$(BUILD)/%.app: $(VENV)/bin/py2applet setup.py $(SRC)/%.py
	$(VENV)/bin/$(PYTH) setup.py py2app --app="['src/$*.py']"

setup.py: $(VENV)/bin/py2applet
	$(VENV)/bin/py2applet --make-setup -a -s --site-packages --packages=PySide -d $(BUILD) -b $(BUILD)

$(VENV)/bin/py2applet: requirements

requirements: pip

pip: $(VENV)/pip-selfcheck.json 

$(VENV)/pip-selfcheck.json: $(VENV) requirements.txt
	$(VENV)/bin/pip install -U pip
	$(VENV)/bin/pip install -Ur requirements.txt
	$(VENV)/bin/$(PYTH) $(VENV)/bin/pyside_postinstall.py -install # dont think needed but ok
	touch $(VENV)/pip-selfcheck.json

$(VENV):
	virtualenv $(VENV) --python=$(PYTH)
	rm -f $(VENV)/pip-selfcheck.json

clean: 
	rm -rf $(BUILD)
