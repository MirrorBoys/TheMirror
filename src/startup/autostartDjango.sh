#!/bin/bash

cd ~/TheMirror
git pull

cd ~/TheMirror/src/smartMirrorProject
pip install -r ~/TheMirror/src/smartMirrorProject/requirements.txt --no-cache-dir
source ~/.virtualEnvs/theMirrorEnv/bin/activate
python3 manage.py  runserver 0.0.0.0:8000 &

exit 0
