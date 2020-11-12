#!/usr/bin/env bash

# NOTE: This file should be copied to /etc/profile.d/ directory
#       And all other files of this project should be copied to /etc/parental-control/ folder


# Configurations
PLC_DIR=/etc/parental-control
PLC_CFG=${PLC_DIR}/parental-control.cfg

# Debug message
echo "Running parental-control.sh!"

# Configuration file handling
if [[ -r ${PLC_CFG} ]]
    then
        # Check if Python is installed
        if command -v python3 &>/dev/null; then
            python3 --version
        else
            echo "*** Error ***: Python 3 is not installed, please install"
            exit -1
        fi
else
    echo "${PLC_CFG} not found! Please run install script!"
    exit -1
fi

# Do parental control login functions in Python
python3 ${PLC_DIR}/parental-control.py $PLC_CFG

