# Development
This document describes relevant information for developers. This includes
- [Development setup](#development-setup): which tools to use and how to install these
- [File structure](#file-structure): the organization of the files in this repository
- [Branch strategy](#branch-strategy): the way we use and organize branches 
- [Contributing instructions](#contributing-instructions): how to contribute to this project

## Development setup
This paragraph outlines our development setup. We use standardized setups to prevent unexpected issues and streamline development.

### Software
We use Django to build web apps. This framework runs on Ubuntu server which is virtualized in Windows Subsystem for Linux (WSL). As editor we use Visual Studio Code (VS Code) with several extensions.

| Software | Version |
|---------|-------------|
|[WSL](https://learn.microsoft.com/en-us/windows/wsl/)|2.3.24|
|[Ubuntu server](https://ubuntu.com/server)|24.04.1|
|[Python](https://www.python.org/)|3.12.3|
|[Django](https://www.djangoproject.com/)|5.1.3|
|[VS Code](https://code.visualstudio.com/)|1.95.1|

#### VS Code extensions
We use these VS Code extensions. These are installed on both the instances of VS Code (local and WSL). All these extensions are optional except the WSL extension.

| Extension|
|--------|
| [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter) |
| [GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) |
| [GitHub Copilot Chat](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat) |
| [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) |
| [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) |
| [Python Debugger](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy) | 
| [WSL](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl) |
| [Pylint](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint) | 

### Installation
Follow these steps to install and configure the software:

1. Install WSL by following [Microsoft's installation instructions](https://learn.microsoft.com/en-us/windows/wsl/install).
> [!IMPORTANT]
> By default, the installed Linux distribution will be the latest stable version of Ubuntu server. Use `wsl --install -d Ubuntu-24.04` instead of `wsl --install` to install this specific version of Ubuntu server.
2. Open an Ubuntu terminal by starting the newly installed `Ubuntu 24.04.1 LTS` Windows app and configure a username and password.
3. Update Ubuntu:
```shell
sudo apt update
sudo apt full-upgrade -y
```
4. Install and configure VS Code on the host machine by following [Microsoft's installation instructions](https://code.visualstudio.com/docs/setup/setup-overview).
5. Install and configure the VS Code extensions.
> [!TIP]
> See [VS Code's documentation](https://code.visualstudio.com/docs/remote/wsl) for instructions on how to develop in WSL using VS Code.
6. Clone this repository to your home directory. The repository will be located at `~/TheMirror`.
```shell
cd
git clone https://github.com/MirrorBoys/TheMirror.git
```
> [!TIP]
> Refer to [VS Code's instructions](https://code.visualstudio.com/docs/sourcecontrol/overview#_cloning-a-repository) if you want to clone the repository with the VS Code GUI or if you run into problems.

7. Create an Python environment in Ubuntu and install the needed packages (including Django)
  
  7.1 Install `python3-venv` to allow the creation of [Python enviroments](https://docs.python.org/3/tutorial/venv.html). 
```shell 
sudo apt install python3-venv
```
7.2 Create an environment in your home directory called `theMirrorEnv`.
```shell
python3 -m venv ~/.virtualEnvs/theMirrorEnv
```
7.3 Enter the enviroment you just created.
```shell
source ~/.virtualEnvs/theMirrorEnv/bin/activate
```
> [!NOTE]
> You can leave the environment by running the `deactivate` command. For this tutorial you must not leave the environment.
  
7.4 Update pip.
```shell
python3 -m pip install --upgrade pip
```
7.5 Install the needed packages using the `requirements.txt` file.
```shell
pip install -r ~/TheMirror/src/smartMirrorProject/requirements.txt --no-cache-dir
```
> [!NOTE]
> The `requirements.txt` file contains a list of multiple packages (including Django) and their respective versions. See [the pip documentation](https://pip.pypa.io/en/stable/reference/requirements-file-format/) for more details.

Your development setup is now ready! See the [contributing instructions](#contributing-instructions) to learn how to contribute to this project.

## File structure
This paragraph gives a brief, global overview of the file structure of this project. 

```shell
.
├── docs
├── .git
│   └── # Configuration folders for Git
├── .github
│   ├── ISSUE_TEMPLATE
│   └── workflows
└── src
    └── smartMirrorProject
        └── smartMirror
```
> [!TIP]
> You can easily generate such a folder tree by running `tree -a -d` in your shell.

This table describes the function of each folder.

| Folder |  Function|
| ----------- | ----------- |
| `docs` | Documentation |
| `.git` | Git configuration | 
| `.github` | GitHub configuration |
| `.github/ISSUE_TEMPLATE` | Templates for GitHub issues |
| `.github/workflows` | [GitHub workflows](https://docs.github.com/en/actions/writing-workflows) |
| `src` | Source code |
| `src/smartMirrorProject` | Source code for Django files |

## Branch strategy
> [!NOTE]
> This information has not been documented yet. Please see [#9](https://github.com/MirrorBoys/TheMirror/issues/9) for the current status of this documentation.

## Contributing instructions
This paragraph outlines how you can contribute to this project.

> [!IMPORTANT]
> If you want to contribute to this project, first install and configure the software needed as outlined in [development setup](#development-setup).

### Contributing to Django files
The Django project files are located in the `src/smartMirrorProject` directory of the repository (or `~/TheMirror/src/smartMirrorProject` in your local repository). You will be editing these files when contributing to the Django files. But first you will have to start the Django server.

#### Start the Django server
> [!IMPORTANT]
> You will need to be in the environment that you have previously created in the [development setup](#development-setup)!

> [!IMPORTANT]
> You will need run these steps every time you pull from the repository. This will ensure that you have installed all the needed packages and migrate changed databases!

1. If present, install newly added packages
```shell
pip install -r ~/TheMirror/src/smartMirrorProject/requirements.txt
```
2. Navigate to the Django project files.
```shell
cd ~/TheMirror/src/smartMirrorProject
```
3. Migrate the models
```shell
python3 manage.py migrate
```
4. Start the Django server.
```shell
python3 manage.py runserver
```

The server is now running and you can view it by visiting [http://127.0.0.1:8000](http://127.0.0.1:8000).

#### Edit Django project files
You can now edit the Django project files. Edits to this files should be directly reflected, with the exception of the `settings.py` file. When editing this file you will need to restart the server.

When you are satisfied with your changes, you can commit (and push) these changes to the repository.

> [!WARNING]
> If you have made changes to the models or updated packages, you need to execute additional steps before committing your changes. See [changed models](#changed-models) and/or [updated packages](#updated-packages).

###### Changed models
Follow these steps if you have edited, added or deleted models.

1. Navigate to the Django project files.
```shell
cd ~/TheMirror/src/smartMirrorProject
```
2. Create migrations for possible changes in the models
```shell
python3 manage.py makemigrations
```
> [!NOTE]
> If changes in existing models are detected by Django, it will prompt you with the question if you want to apply them. 

###### Updated packages
Follow these steps if you have added or deleted pip packages.

1. Navigate to the Django project files.
```shell
cd ~/TheMirror/src/smartMirrorProject
```
2. Generate a new `requirements.txt` file.
```shell
pip freeze > requirements.txt
```
