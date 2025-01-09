# This script is partly generated with AI (ChatGTP and CoPilot)

# This script will run all the commands in the `command` variable. It is used to update pip and it's respective
# packages and 'reset' Django. Typically one runs this script after switching branches to ensure everything
# is up-to-date, all needed packages are installed and (new) models are made.

import os
import subprocess


def executeCommand(command, captureOutput=True):
    """
    Executes a shell command.

    Parameters:
    command (str): The command to execute.
    capture_output (bool): If True, captures and prints the command's stdout and stderr. Defaults to True.

    """
    if captureOutput:
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
    # Upgrade pip
    "python3 -m pip install --upgrade pip",
    # Install all packages in `requirements.txt`
    "pip install -r ~/TheMirror/src/smartMirrorProject/requirements.txt --no-cache-dir",
    # Remove old migration files
    'find . -path "*/migrations/*.py" -not -name "__init__.py" -delete',
    'find . -path "*/migrations/*.pyc" -delete',
    # Delete database
    "rm ~/TheMirror/src/smartMirrorProject/db.sqlite3",
    # Generate new migration files
    "python3 ~/TheMirror/src/smartMirrorProject/manage.py makemigrations",
    # Run migrations
    "python3 ~/TheMirror/src/smartMirrorProject/manage.py migrate",
    # Run script that creates testusers
    "python3 ~/TheMirror/src/smartMirrorProject/manage.py runscript create_test_users",
]

for command in commands:
    if "runserver" in command:
        executeCommand(command, captureOutput=False)
    else:
        executeCommand(command)
