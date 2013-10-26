#!/bin/bash

set -o errexit
set -o nounset

repo=$(realpath "$(dirname "$(realpath -- "${BASH_SOURCE[0]}")")/..")
cd -- "${repo}/test"

mrt "${@}"

