#!/bin/sh

cd $1
./autogen.sh
PYTHON=python3 ./configure
make -j4
sudo checkinstall -D --install=no --addso --nodoc --pkgversion 0$(git rev-parse --short HEAD) --default
