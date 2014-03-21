#!/usr/bin/env zsh

setopt ERR_EXIT
setopt NO_UNSET


# ==============================================================================
# = Configuration                                                              =
# ==============================================================================

# Paths

repo=$(realpath -- ${0:h}/..)

venv=$repo/local/venv


# Packages

pacman_packages=(
    git
    python2-virtualenv
    zsh
)


# ==============================================================================
# = Tasks                                                                      =
# ==============================================================================

function install_pacman_packages()
{
    sudo pacman --noconfirm --sync --needed --refresh $pacman_packages
}

function create_virtualenv()
{
    mkdir --parents $venv:h
    virtualenv --python=python2.7 $venv
}

function install_python_packages()
{
    unsetopt NO_UNSET
    source $venv/bin/activate
    setopt NO_UNSET

    python $repo/setup.py develop
}


# ==============================================================================
# = Command line interface                                                     =
# ==============================================================================

tasks=(
    install_pacman_packages
    create_virtualenv
    install_python_packages
)

function usage()
{
    cat <<-'EOF'
		Set up a development environment

		Usage:

		    setup.zsh [TASK...]

		Tasks:

		    install_pacman_packages
		    create_virtualenv
		    install_python_packages
	EOF
    exit 1
}

for task in $@; do
    if [[ ${tasks[(i)$task]} -gt ${#tasks} ]]; then
        usage
    fi
done

for task in ${@:-$tasks}; do
    print -P -- "%F{green}Task: $task%f"
    $task
done

