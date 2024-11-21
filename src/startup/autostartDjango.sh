#!/bin/bash

cd /home/thor/TheMirror
git pull

cd /home/thor/TheMirror/src/smartMirrorProject
source ~/.virtualEnvs/theMirrorEnv/bin/activate
python manage.py  runserver 0.0.0.0:8000 &

exit 0