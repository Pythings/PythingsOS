#!/bin/bash

INSTALLER_DIR="`dirname \"$0\"`"
#echo "Moving to $INSTALLER_DIR"
cd $INSTALLER_DIR
clear

if [ -z "$PYTHON" ]; then
    PYTHON='python'
fi

$PYTHON installer.py
