#!/bin/sh
set -ex
cd ~/src
export PYTHONPATH=$PYTHONPATH:/tmp/usr/local/lib/python2.7/dist-packages
nosetests
