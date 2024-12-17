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
sleep 20

# Start Chromium in kiosk mode
/usr/bin/chromium-browser --start-fullscreen --start-maximized --kiosk --noerrdialogs --disable-default-apps --disable-single-click-autofill --disable-translate-new-ux --disable-translate --disable-cache --disk-cache-dir=/dev/null --disk-cache-size=1 --reduce-security-for-testing --app=http://localhost:8000/ &

# Make sure Chromium stays on top
wmctrl -r "localhost" -b add,above
wmctrl -r "TheMirror" -b add,above


exit 0