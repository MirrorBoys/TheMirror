#!/bin/bash

# Navigate to the main project directory and update the repository
cd ~/TheMirror
git pull

# Navigate to the smart mirror project directory and activate the virtual environment
cd ~/TheMirror/src/smartMirrorProject
source ~/.virtualEnvs/theMirrorEnv/bin/activate

# Install the required Python packages
pip3 install -r ~/TheMirror/src/smartMirrorProject/requirements.txt --no-cache-dir

# Start the Django server
python3 manage.py runserver 0.0.0.0:8000 &

# Run the gesture utility script
python3 ~/TheMirror/src/smartMirrorProject/utilities/gestureUtility/testscript.py &

exit 0