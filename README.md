# MicroPython Scripts for RPi Pico on [BearCar](https://github.com/ucaengineeringphysics/bearcar)

## Prepare
Flash the latest MicroPython firmware to Raspberry Pi Pico board.
For Raspberry Pi Pico 2: download [here](https://micropython.org/download/RPI_PICO2/)

## Installation (Debian-like Linux)
0. Install dependencies and grant user permission to access Pico
  ```console
  sudo apt install python3-pip
  pip install rshell --break-system-packages
  ```

> [!TIP]
> If you are **NOT** on Raspberry Pi OS, enter the following command in terminal then reboot computer.
>
```console
sudo usermod -aG dialout $USER
```

1. Download and dive into the local repository.

  ```console
  cd ~  # can be another location
  git clone https://github.com/ucaengineeringphysics/bearcar_pico.git
  cd bearcar_pico
  ```

2. Upload action and perception modules.

  ```console
  rshell -p /dev/ttyACM0 --buffer-size 512 cp -r upython_scripts/perception /pyboard/
  rshell -p /dev/ttyACM0 --buffer-size 512 cp -r upython_scripts/action /pyboard/
  ```

3. Upload main script.
This will set up automatic communication with the Raspberry Pi or any computer using [`pico_interface.py`](./upython_scripts/pico_interface.py).

  ```console
  rshell -p /dev/ttyACM0 --buffer-size 512 cp upython_scripts/pico_interface.py /pyboard/main.py
  ```

  > [!TIP]
  > A hard reset (unplug Pico then plug it back) is required to activate `main.py`.

> [!IMPORTANT]
> If you are completely new to Pico or MicroPython, please follow the official [guide](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/) to get started.

## Usage

### Calibrate ESC 
> [!TIP]
> Use [Thonny](https://thonny.org/) IDE.

Follow the instructions in [`calibrate_esc.py`](./upython_scripts/calibrate_esc.py).

### LED Indicator
| Mode Name | LED Color |
| :---      |   :---:   |
| Autopilot | Purple    |
| Error     | Red       |
| Normal    | Green     |
| Pause     | Yellow    |
| Recording | Blue      |
| Standby   | Cyan      |
| Other     | Off       |
