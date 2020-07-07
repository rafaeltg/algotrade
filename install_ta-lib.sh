#!/usr/bin/env bash

apt-get install build-essential wget -y
wget https://artiya4u.keybase.pub/TA-lib/ta-lib-0.4.0-src.tar.gz
tar -xvf ta-lib-0.4.0-src.tar.gz

(
  cd ta-lib/
  ./configure --prefix=/usr
  make
  make install
)

rm -rf ta-lib-0.4.0-src.tar.gz ta-lib
apt-get purge -y wget