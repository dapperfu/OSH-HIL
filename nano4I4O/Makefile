# Orchestrate the nano4I4O smoke bench.
VENV := venv_nano4I4O
PYTHON := ${VENV}/bin/python
STRICTDOC := ${VENV}/bin/strictdoc
PIO := pio
DOCS := ocd sss srs irs sdd stp std

.PHONY: help clean build test test-coverage run \
	strictdoc-init strictdoc-generate strictdoc-validate strictdoc-export \
	strictdoc-serve strictdoc-tree strictdoc-help \
	install-completions uninstall-completions

help:
	@echo "make build                  Build HIL and HUT firmware"
	@echo "make test                   Run pytest. Fails when the bench is absent"
	@echo "make run                    Run the same checkout pytest entry point"
	@echo "make clean                  Remove build trees and coverage output"
	@echo "make install-completions    Install nano4i4o shell completions"
	@echo "make strictdoc-generate     Regenerate reqs/html from the .sdoc sources"

clean:
	rm -rf build HIL/.pio HUT/.pio htmlcov .coverage reqs/_cache

build:
	${PIO} run -e read_d2_d5 -e drive_walk --project-dir HIL
	${PIO} run -e read_d2_d5 -e drive_walk --project-dir HUT

test-coverage:
	${PYTHON} -m coverage run -m pytest
	${PYTHON} -m coverage report --fail-under=80
	${PYTHON} -m coverage html

test: test-coverage

run: test

strictdoc-init:
	mkdir -p reqs/ocd reqs/sss reqs/srs reqs/irs reqs/sdd reqs/stp reqs/std reqs/html

strictdoc-generate: strictdoc-init
	cd reqs && ../${STRICTDOC} export ${DOCS} --output-dir ../build/strictdoc
	rm -rf reqs/html
	mkdir -p reqs/html
	cp -a build/strictdoc/html/. reqs/html/

strictdoc-validate:
	cd reqs && ../${STRICTDOC} export ${DOCS} --output-dir ../build/strictdoc-validate

strictdoc-export: strictdoc-generate

strictdoc-serve:
	cd reqs && ../${STRICTDOC} server ${DOCS}

strictdoc-tree:
	find reqs -name '*.sdoc' | sort

strictdoc-help:
	@echo "strictdoc-init strictdoc-generate strictdoc-validate strictdoc-export strictdoc-serve strictdoc-tree"

install-completions:
	${PYTHON} -m nano4i4o completion install --rc

uninstall-completions:
	${PYTHON} -m nano4i4o completion uninstall --rc
