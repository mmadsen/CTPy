#!/bin/sh
set -ex
cd ~/src
export PYTHONPATH=$PYTHONPATH:~/src/usr/local/lib/python2.7/dist-packages
nosetests
