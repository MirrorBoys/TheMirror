# Raspberry Pi installation documentation
The following document describes the relevant information to make the raspberry pi ready for use. 

## Flashing SD card
To put the OS on the SD card the Raspberry Pi imager is used 
### OS
The OS that is used is Raspbian Desktop. The desktop version is used because this enables us to use the kiosk mode of the RPI. 

### Hostname, username and password 
Choose a hostname for the RPI and put in the username and password you want to use. 
![raspberry imager hostname](img/installationRPI/hostname.png)

### Wifi (optional)
If you want to use the RPI over wifi, you can put in the SSID and password of the wifi network you want to use. The RPI will then automatically connect to this wifi network. 

![raspberry imager wifi](img/installationRPI/wifi.png)

### SSH (optional)

It's also possible to give an SSH key for login during the flashing of the SD card. To do this select the option for ssh key under services and put in your public ssh key.

![raspberry imager ssh](img/installationRPI/ssh.png)

## Getting ready to use python

### Startup
After the RPI is started and you are connect to the RPI you run the following commands to update the RPI

```
sudo apt update
```
```
sudo apt upgrade -y
```

### Python 

Check if a version of Python is installed 
```
python3 --version
```
If not, install Python
```
sudo apt install python3 -y
```

To make it possible to install and use Python libaries install pip3 and venv
```
sudo apt install python3-pip python3-venv
```
 
Create a directory for the mirror project and the Python environment
```
mkdir ~/.virtualEnvs/theMirrorEnv
```

Create the Python environment
```
python -m venv ~/.virtualEnvs/theMirrorEnv
```

### Clone repository 
To clone the repository into your home directory
```
cd
git clone https://github.com/MirrorBoys/TheMirror.git
```
this will create a directory named TheMirror with all the files from GitHub in it

### Pip
To make it possible to use the different libraries that are used in the project the libraries need to be installed into a Python environment. 

First start the environment you created
```
source <dir>/bin/activate
``` 

To deactivate the environment:
```
deactivate
```

When you have activated the environment use the requirements.txt to install all required libraries
```
pip install -r ~/TheMirror/src/smartMirrorProject/requirements.txt
```

## Enable Serial Peripheral Interface
Serial Peripheral Interface (SPI) is neseccary for communicating with the NFC reader. This is disabled by default and therefore has to be enabled manually.

1. Open de `raspi-config` utility.
```shell
sudo raspi-config
```
2. Select `3 Interface Options`
3. Select `I4 SPI`
4. Enable SPI
5. Reboot the Raspberry Pi to enable the interface.
```shell
sudo reboot now
```

## All done 

With this the RPI should be ready to be used. If you want to run the mirror you can use the following commands to start the web server: 

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
This will start the project and it will be visible on the RPI and can be viewed by visiting 127.0.0.1:8000 or localhost:8000 

To make it so that the webserver can be visited by external devices use the following command 
```
python manage.py runserver 0.0.0.0:8000
```
The webserver can then be visited by other devices on the network by visiting: ipAddressOffRPI:8000

This can give the error that the IP address of the device needs to be added to the ALLOWED_HOSTS in settings.py
![allowed_hosts](img/installationRPI/allowed_hosts.png)

