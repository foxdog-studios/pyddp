# =============================================================================
# = Configuration                                                             =
# =============================================================================

repo=$(realpath "$(dirname "$(realpath -- "${BASH_SOURCE[0]}")")/../..")

env=${repo}/env

node_global_packages=(
    'meteorite'
)

python_packages=(
    'ws4py==0.3.2'
)

python_version=2.7

system_packages=(
    'git'
    'python2-virtualenv'
)


# =============================================================================
# = Tasks                                                                     =
# =============================================================================

create_ve() {
    "virtualenv-${python_version}" "${env}"
}

install_global_node_packages() {
    sudo --set-home npm install --global "${node_global_packages[@]}"
}

install_python_packages() {
    _ve _install_python_packages
}

_install_python_packages() {
    local package
    for package in "${python_packages[@]}"; do
        pip install "${package}"
    done
}

install_system_packages() {
    sudo pacman --needed --noconfirm --refresh --sync "${system_packages[@]}"
}


# =============================================================================
# = Helpers                                                                   =
# =============================================================================

_allow_unset() {
    local restore=$(set +o | grep nounset)
    set +o nounset
    "${@}"
    local exit_status=${?}
    # Do not quote, expansion is desired
    ${restore}
    return "${exit_status}"
}

_ve() {
    _allow_unset source "${env}/bin/activate"
    "${@}"
    _allow_unset deactivate
}

