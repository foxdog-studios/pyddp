#!/bin/bash

set -o errexit
set -o nounset


# =============================================================================
# = Command line interface                                                    =
# =============================================================================

usage() {
    echo '
    Install dependencies and set up development environment

    Usage:

        arch.sh
'
    exit 1
}

while getopts : opt; do
    case "${opt}" in
        \?|*) usage ;;
    esac
done

shift $(( OPTIND - 1 ))

if [[ "${#}" != 0 ]]; then
    usage
fi


# =============================================================================
# = Tasks                                                                     =
# =============================================================================

repo=$(realpath "$(dirname "$(realpath -- "${BASH_SOURCE[0]}")")/../..")
cd -- "${repo}"

source scripts/setup/arch-tasks.sh

install_system_packages
create_ve
install_python_packages
install_global_node_packages

