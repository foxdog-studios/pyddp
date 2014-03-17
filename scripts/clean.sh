#!/usr/bin/env sh

cd "$(dirname "$0")/.."
rm -fr build dist pyddp.egg-info *.egg
find -name '*.pyc' -exec rm {} \;

