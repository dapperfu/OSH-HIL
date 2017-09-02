venv:
	python3 -mvenv --system-site-packages venv

.PHONY: pip
pip:
	pip install -U -r requirements_venv.txt
	pip install -U -r requirements_uhil.txt

.PHONY: debian
debian:
	sudo apt-get install python3-venv libusb-1.0-0

.PHONY: clean
clean:
	rm -rf venv

crossbuild:
	# Still WIP. May be broken.

	# Run on desktop machine to speed up cross compiling for the Pi.
	# Requires apt-cacher-ng if you are going to use http://127.0.0.1:3142
	sudo debootstrap --foreign --no-check-gpg --include=ca-certificates --arch=armhf stretch crossbuild http://127.0.0.1:3142/archive.raspbian.com/raspbian
	sudo cp $(which qemu-arm-static) crossbuild/usr/bin
	sudo chroot crossbuild/ /debootstrap/debootstrap --second-stage --verbose


.PHONY: libserialport
libserialport:
	git clone "git://sigrok.org/libserialport"
	./sigrok_dpkg.sh libserialport

.PHONY: libsigrok
libsigrok:
	git clone git://sigrok.org/libsigrok
	./sigrok_dpkg.sh libsigrok

.PHONY: libsigrokdecode
libsigrokdecode:
	git clone git://sigrok.org/libsigrokdecode
	./sigrok_dpkg.sh libsigrokdecode

.PHONY: sigrok-cli
sigrok-cli:
	git clone git://sigrok.org/sigrok-cli
	./sigrok_dpkg.sh sigrok-cli

#libserialport/configure: libserialport
#	cd libserialport && ./autogen.sh

#libserialport/Makefile: libserialport/configure
#	cd libserialport && ./configure

#libserialport/.libs/libserialport.so:
#	cd libserialport && make -j4

#libserialport/libserialport.deb:
#	cd libserialport && sudo checkinstall -D --install=no --addso --nodoc --pkgversion $(git rev-parse --short HEAD) --default
#	mv libserialport/libserialport*.deb libserialport/libserialport.deb
