#!/bin/bash
export DISPLAY=:0
# Navigate to the main project directory and update the repository
cd ~/TheMirror
git checkout 126-req-43-de-spiegel-bevat-een-camera-voor-bediening-via-gebaren
git pull

# Navigate to the smart mirror project directory and activate the virtual environment
cd ~/TheMirror/src/smartMirrorProject
source ~/.virtualEnvs/theMirrorEnv/bin/activate

# Install the required Python packages
pip3 install -r ~/TheMirror/src/smartMirrorProject/requirements.txt --no-cache-dir

# Start the Django server
python3 manage.py runserver 0.0.0.0:8000 &

# Run the gesture utility script
lxterminal -e "bash -c 'source ~/.virtualEnvs/theMirrorEnv/bin/activate; python3 ~/TheMirror/src/smartMirrorProject/utilities/gestureUtility/testscript.py; echo \"Press any key to close\"; read'" &

# Sleep for a moment to ensure the terminal is open
#sleep 30

# Make sure Chromium stays on top
#wmctrl -a "localhost"
#wmctrl -a "TheMirror"
#wmctrl -r "Frame" -b add,hidden
#wmctrl -r "testscript.py" -b add,hidden 
#wmctrl of xdotool zien beide geen windows of tabs van chromium, hierdoor is het niet gelukt om een tab naar voren of achter te brengen
exit 0