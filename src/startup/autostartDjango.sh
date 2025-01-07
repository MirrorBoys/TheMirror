#!/bin/bash

export DISPLAY=:0

# Get the directory of the current script
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

# Redirect all output to a log file in the same directory as the script
LOG_FILE="$SCRIPT_DIR/autostart.log"
exec > "$LOG_FILE" 2>&1

# Navigate to the main project directory and update the repository
cd ~/TheMirror
git checkout 190-realiseren-achterliggende-functies-voor-gebaren
git pull

# Navigate to the smart mirror project directory and activate the virtual environment
cd ~/TheMirror/src/smartMirrorProject
source ~/.virtualEnvs/theMirrorEnv/bin/activate

# Install the required Python packages
pip3 install -r ~/TheMirror/src/smartMirrorProject/requirements.txt --no-cache-dir

# Start the Django server
python3 manage.py runserver 0.0.0.0:8000 &
