#!/usr/bin/env zsh

setopt ERR_EXIT
setopt NO_UNSET

cd -- ${0:h}/..

unsetopt NO_UNSET
source local/venv/bin/activate
setopt NO_UNSET

python setup.py clean sdist bdist_wheel check
twine upload dist/*

