#!/bin/bash

cd ~/TheMirror
git pull

cd ~/TheMirror/src/smartMirrorProject
source ~/.virtualEnvs/theMirrorEnv/bin/activate
pip3 install -r ~/TheMirror/src/smartMirrorProject/requirements.txt --no-cache-dir
python3 manage.py  runserver 0.0.0.0:8000 &

exit 0
