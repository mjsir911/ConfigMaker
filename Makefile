MAKEFLAGS += --warn-undefined-variables
RM += -r

PYTH = python2.7
VENV = venv/
BUILD = build/
DIST_DIR=dist/
TARGET = ratings.app presets.app
TARGET := $(addprefix $(DIST_DIR)/,$(TARGET))
SRC = src/

.DEFAULT_GOAL := build
.PHONY: build
build: $(TARGET)

$(DIST_DIR)/%.app: %.spec $(SRC)/%.py $(SRC)/UI | $(VENV)/bin/pyinstaller
	$| --noconfirm $*.spec

$(SRC)/UI:
	echo '$@ needs to exist!'
	exit 2

$(SRC)/%.py: $(SRC)/shared.py

%.spec: $(SRC)/%.py $(SRC)/style.css | $(VENV)/bin/pyi-makespec
	$| -w --add-data "$(word 2,$^):." $<

$(VENV)/bin/pyi-makespec: $(VENV)/bin/pyinstaller
$(VENV)/bin/pyinstaller: requirements

requirements: pip

pip: $(VENV)/pip-selfcheck.json 

$(VENV)/pip-selfcheck.json: $(VENV) requirements.txt
	$(VENV)/bin/pip install -U pip
	$(VENV)/bin/pip install -Ur requirements.txt
	$(VENV)/bin/$(PYTH) $(VENV)/bin/pyside_postinstall.py -install # dont think needed but ok
	touch $(VENV)/pip-selfcheck.json

$(VENV):
	virtualenv --python=$(PYTH) $@
	$(RM) $(VENV)/pip-selfcheck.json

.PHONY: clean
clean: 
	$(RM) $(BUILD) $(DIST_DIR) *.spec
