#!/bin/bash

install_poetry() {
    if ! [ -f ~/.local/bin/poetry ]; then
        echo "Installing Poetry"
        curl -sSL https://install.python-poetry.org | python3 -
    fi
}

install_pyenv() {
    if [[ "$(uname)" =~ ^(Linux|Darwin)$ ]]; then
        if ! [ -d ~/.pyenv ]; then
            echo "Installing pyenv"
            curl https://pyenv.run | bash
        fi
    else
        echo "Error: currently pyenv installation is only supported on Linux/Unix systems"
        exit 1
    fi
}