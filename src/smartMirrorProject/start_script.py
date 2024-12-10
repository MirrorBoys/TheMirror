# Generated with CoPilot

import os
import subprocess


def execute_command(command, capture_output=True):
    if capture_output:
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print(f"Error executing command: {command}\n{stderr.decode()}")
        else:
            print(f"Command executed successfully: {command}\n{stdout.decode()}")
    else:
        process = subprocess.Popen(command, shell=True)
        process.communicate()


commands = [
    "python3 -m pip install --upgrade pip",
    "pip install -r ~/TheMirror/src/smartMirrorProject/requirements.txt --no-cache-dir",
    "python3 manage.py migrate",
    "python3 manage.py runscript create_test_user",
    "python3 manage.py runserver 0.0.0.0:8000",
]

for command in commands:
    if "runserver" in command:
        execute_command(command, capture_output=False)
    else:
        execute_command(command)
