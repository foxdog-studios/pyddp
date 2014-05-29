#!/usr/bin/env sh

sudo pacman --noconfirm --sync --needed --refresh zsh
exec zsh "$(dirname "$(realpath -- "${BASH_SOURCE[0]}")")/setup.zsh" "$@"

