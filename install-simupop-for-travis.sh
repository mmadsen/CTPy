#!/bin/sh
set -ex
cd /tmp
wget --no-check-certificate http://iweb.dl.sourceforge.net/project/simupop/simupop/1.1.2/simuPOP-1.1.2.Ubuntu13-x86_64.tar.gz -O /tmp/simupop-1.1.2.tar.gz
tar -xzvf simupop-1.1.2.tar.gz
cd simuPOP-1.1.2.Ubuntu13-x86_64
sudo python setup.py install

