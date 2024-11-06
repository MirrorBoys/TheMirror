# Development setup
This paragraph describes our development setup. We use identical setups to prevent unexpected issues and streamline development.

## Software
We use Django to build web apps. This framework runs on Ubuntu server which is virtualized in Windows Subsystem for Linux (WSL). As editor we use Visual Studio Code (VS code) with several extensions.

| Software | Version |
|---------|-------------|
|[WSL](https://learn.microsoft.com/en-us/windows/wsl/)|2.3.24|
|[Ubuntu server](https://ubuntu.com/server)|24.04.1|
|[Python](https://www.python.org/)|3.12.3|
|[Django](https://www.djangoproject.com/)|5.1.3|
|[VS code](https://code.visualstudio.com/)|1.95.1|

### VS code extensions
We use these VS code extensions. These are installed on both the instances of VS code (local and WSL).

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

## Installation
Follow these steps to install and configure the software:

1. Install WSL by following [Microsoft's installation instructions](https://learn.microsoft.com/en-us/windows/wsl/install).
> [!IMPORTANT]
> By default, the installed Linux distribution will be the latest stable version of Ubuntu server. Use `wsl --install -d Ubuntu-24.04` instead of `wsl --install` to install this specific version of Ubuntu server.
2. Open a Ubuntu terminal by starting the newly installed `Ubuntu 24.04.1 LTS` Windows app and configure a username and password.
3. Update Ubuntu:
```shell
sudo apt update
sudo apt full-upgrade -y
```
4. Install VS code on the host machine by following [Microsoft's installation instructions](https://code.visualstudio.com/docs/setup/setup-overview).
5. Install and configure the VS code extensions.
> [!TIP]
> The most important extension is WSL. See [VS code's documentation](https://code.visualstudio.com/docs/remote/wsl) for instructions on how to use develop in WSL and VS code.
6. Create an Python environment on Ubuntu and install Django.
  - Install `python3-venv` to allow the creation of [Python enviroments](https://docs.python.org/3/tutorial/venv.html).
```shell
sudo apt install python3-venv
```
  - Create an environment at a specified path by running `python3 -m venv /<example>/<path>`.
```shell
python3 -m venv ~/django
```
  - Enter the enviroment you just created by running `source /<example>/<path>/bin/activate`
```shell
source ~/django/bin/activate
```
> [!TIP]
> You can leave the enviroment by running the `deactivate` command.
  - Update pip
```shell
python3 -m pip install --upgrade pip
```
  - Use pip to install Django
```shell
python3 -m pip install Django
```

# File structure
TODO: [#10](https://github.com/MirrorBoys/TheMirror/issues/10)

# Branches
TODO: [#9](https://github.com/MirrorBoys/TheMirror/issues/9)
