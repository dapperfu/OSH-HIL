YAMLS:=$(wildcard *.yaml)
BUILD_DIRS=$(patsubst %.yaml,%,${YAMLS})

# Configuration
PYTHON_VENV?=.venv
PYTHON_VER?=python3.7
PYTHON_BIN?=$(shell which ${PYTHON_VER})

.PHONY: debug
debug:

	$(info $${YAMLS}=${YAMLS})
	$(info $${BUILD_DIRS}=${BUILD_DIRS})
	$(info $${PYTHON_VER}=${PYTHON_VER})
	$(info $${PYTHON_VENV}=${PYTHON_VENV})
	$(info $${PYTHON_BIN}=${PYTHON_BIN})

.PHONY: all
all: ${BUILD_DIRS}

%: %.yaml
	${PYTHON_VENV}/bin/esphome ${^} compile

.PHONY: flash-all
flash-all:
	ls *.yaml | xargs -P8 -n1 -I{} ${PYTHON_VENV}/bin/esphome {} upload

.PHONY: clean
clean:
	rm -rf ${BUILD_DIRS}
	
.PHONY: clean-all
clean-all:
	${MAKE} clean
	rm -rf ${PYTHON_VENV}
	
.PHONY: venv
venv: ${PYTHON_VENV}/bin/python

${PYTHON_VENV}/bin/python:
	${MAKE} debug
	${PYTHON_BIN} -mvenv ${PYTHON_VENV}
	${PYTHON_VENV}/bin/pip install --upgrade wheel setuptools pip
	${PYTHON_VENV}/bin/pip install -r requirements.txt
