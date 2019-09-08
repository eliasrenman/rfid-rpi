# RFID PI
#### WARNING This repository is W.I.P and all features of the program does not work proceed at your own risk!

Physical check in and out system written to work with [Yogster's](https://github.com/Yogsther) rest api and web interface

[Link to Rest api and web interface](https://github.com/Yogsther/te4-time)

## Hardware needed
- Raspberry pi 3 or newer.
- RC522 RFID module
- 4 Leds
- 4 Resistors
## Software needed
- Python 3.7 or newer
- Python3 pip
- SSH (Optional but recommended)
- git
- SPI needs to be enabled ([guide](https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial/all#spi-on-pi))
## Python dependencies
- [SimpleMFRC522](https://github.com/pimylifeup/MFRC522-python)
- Spidev
- RPi.GPIO
- [dotenv](https://github.com/theskumar/python-dotenv)
# Installation
Before using this program make sure that the GPIO pins are correctly wired as incorrectly wired components *CAN* 
brick your Raspberry or components so proceed at your own risk.

## Wiring
Turn off your Rpi and connect the cables according to the picture and schematics.

####Warning! These schematics currently don't include wiring for the LEDS

![visual image](https://raw.githubusercontent.com/Abborren/rfid-rpi/master/images/visual.png)

![schematics](https://raw.githubusercontent.com/Abborren/rfid-rpi/master/images/schematics.png)


#### Remember to enable SPI and double check the wiring! 
### Software preparation
install the python dependencies by writing ``pip3 install `` and the package name.
### Software cloning and installation
After correctly doing the previous steps you can now start with the software by cloning and opening the directory.

`git clone https://github.com/Abborren/rfid-rpi`

`cd dir rfid-rpi`

After entering the directory copy the .env.example to .env.

`cp .env.example .env`

Edit the .env file and add the needed values.
```dotenv
# HTTP REQUEST VARIABLES
TOKEN=              # A token value that the rest api uses to validate the http request
HOST_ENDPOINT=      # URL + /api/check if the running rest api is Yogster's
PORT=443            # Should preferably be 443 for https
# GENERAL ENV
DEBUG_INPUT=true    # This is used when debugging the program without a RPI or rfid reader
DEBUG_OUTPUT=true   # This is used to console log output instead of blinking leds
CONSOLE_PRINT=true  # This enables or disables console printing
```

If all the wiring is correct, spi is enabled and all the python dependencies are installed the program should be ready to run.
Run the program by writing:
``
sudo python3 run.py
``