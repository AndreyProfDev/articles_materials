#!/bin/bash

COMPONENT_NAME=$1
COMPONENT_FOLDER=$2

cd $COMPONENT_FOLDER

if ! [ -f ./pyproject.toml ]; then
    echo "Creating environment for $COMPONENT_NAME in $COMPONENT_FOLDER"

    touch README.md
    poetry init --name $COMPONENT_NAME
fi