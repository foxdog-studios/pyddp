#!/usr/bin/env bash

set -o errexit
set -o nounset


repo=$(realpath "$(dirname "$(realpath -- "${BASH_SOURCE[0]}")")/..")
cd -- "${repo}"

function is_listening()
{
    curl http://localhost:3000/ &> /dev/null
}

if ! is_listening; then
    echo -n 'Launching test Meteor server.'

    function clean_up()
    {
        if [[ -v pid ]]; then
            kill "${pid}" &> /dev/null || true
        fi
    }

    trap clean_up EXIT

    "${repo}/scripts/mrt.sh" &> /dev/null &
    pid=${?}

    until is_listening; do
        echo -n '.'
        sleep 0.1
    done

    echo 'done'
fi

set +o nounset
source env/bin/activate
set -o nounset

export "PYTHONPATH=${repo}/src"
python test.py "${@}"

