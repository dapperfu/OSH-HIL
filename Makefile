venv:
	python3 -mvenv venv

.PHONY: pip
pip:
	pip install -U -r requirements_venv.txt
	pip install -U -r requirements_uhil.txt

.PHONY: debian
debian:
	sudo apt-get install python3-venv

.PHONY: clean
clean:
	rm -rf venv
