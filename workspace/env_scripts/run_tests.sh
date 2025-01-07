#!/bin/bash

COMPONENT_FOLDER=$1

cd $COMPONENT_FOLDER

if [ -d "tests" ]; then
    poetry run python -m unittest
fi
