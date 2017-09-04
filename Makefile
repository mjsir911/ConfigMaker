PYTH = python2.7
VENV = venv/
BUILD = build/
TARGET = ratings.app presets.app
TARGET := $(addprefix $(BUILD)/,$(TARGET))
SRC = src/



.PHONY: all build clean $(APP)

#$(VENV)/bin/py2applet -s -d build/ src/makeconf.py
#rm -rf $(BUILD)/bdist*
#"build/makeconf-$(shell date -u +"%Y-%m-%d").app"
all: $(VENV) $(BUILD)

build: $(TARGET)


$(BUILD)/%.app: setup.py $(SRC)/%.py $(SRC)/UI | $(VENV)/bin/py2applet
	$(VENV)/bin/$(PYTH) setup.py py2app --app="['$(SRC)/$*.py']"

$(SRC)/UI:
	echo '$(SRC)/UI needs to exist!'
	exit 2

setup.py: | $(VENV)/bin/py2applet
	$(VENV)/bin/py2applet --make-setup -a -s --site-packages --resources='src/' --packages=PySide -d $(BUILD) -b $(BUILD) $(SRC)
	#$(VENV)/bin/py2applet --make-setup --resources='src/' -d $(BUILD) -b $(BUILD) $(SRC)

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
