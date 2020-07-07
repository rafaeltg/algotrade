#!/usr/bin/env bash

apt-get install git -y
git clone https://github.com/rafaeltg/pydl.git

(
  cd pydl
  pip install pip -U
  pip3 install --no-cache-dir -r requirements.txt -U
  pip3 install --no-cache-dir tensorflow
  python3 setup.py install -O2
)

rm -rf pydl
apt-get purge -y git