# Configuration
PYTHON_VER?=python3.8
PYTHON_VENV?=virtualenv_${PYTHON_VER}
PYTHON_BIN?=$(shell which ${PYTHON_VER})

.PHONY: all
all:
	@echo "Please select from one of the below targets:"
	@echo "--------------------------------------------"
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'
	
.PHONY: debug
debug:
	$(info $${PYTHON_VER}=${PYTHON_VER})
	$(info $${PYTHON_VENV}=${PYTHON_VENV})
	$(info $${PYTHON_BIN}=${PYTHON_BIN})
	
.PHONY: clean-all
clean-all:
	${MAKE} clean
	rm -rf ${PYTHON_VENV}
	
.PHONY: venv
venv: ${PYTHON_VENV}/bin/python

${PYTHON_VENV}/bin/python:
	${PYTHON_BIN} -mvenv ${PYTHON_VENV}
	${PYTHON_VENV}/bin/pip install --upgrade pip wheel
	${PYTHON_VENV}/bin/pip install -r requirements.txt

.PHONY: host
host:
	# Host Target
	# Setup the host
	# Tested on Ubuntu 18.04
	sudo apt-get install python3.8-minimal python3.8-dev python3.8-venv

clone_components.sh: make_clone_components.sh
	echo '#!/usr/bin/env bash'
	./${^} > ${@}
	chmod +x ${@}
