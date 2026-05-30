# MicroPython Scripts for RPi Pico on [BearCar](https://github.com/ucaengineeringphysics/bearcar)


## Usage (Linux)
0. Install dependencies and grant user permission to access Pico
  ```console
  sudo apt install python3-pip
  pip install rshell
  sudo usermod -aG dialout $USER
  ```

  > [!TIP]
  > Reboot computer to gain access unless you are on RPiOS.

1. Download and dive into the local repository.

  ```console
  cd ~  # can be another location
  git clone https://github.com/ucaengineeringphysics/bearcar_pico.git
  cd bearcar_pico
  ```

2. Upload motion and perception controller 

  ```console
  rshell -p /dev/ttyACM0 --buffer-size 512 cp -r upython_scripts/perception /pyboard/
  rshell -p /dev/ttyACM0 --buffer-size 512 cp -r upython_scripts/action /pyboard/
  ```

3. Set up automatic communication with the Raspberry Pi or any computer using [`pico_interface.py`](./upython_scripts/pico_interface.py).

  ```console
  rshell -p /dev/ttyACM0 --buffer-size 512 cp upython_scripts/pico_interface.py /pyboard/main.py
  ```

  > [!TIP]
  > A hard reset (unplug Pico then plug it back) is required to activate `main.py`.

> [!IMPORTANT]
> If you are completely new to Pico or MicroPython, please follow the official [guide](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/) to get started.

4. Calibrate ESC following the instructions in [`calibrate_esc.py`](./upython_scripts/calibrate_esc.py).
  > [!TIP]
  > Use [Thonny](https://thonny.org/) IDE.

## Test

```console
cd ~/homer_pico/
python3 tests/computer_messenger.py
```


## LED Indicator
| Mode Name | LED Color |
| :---      |   :---:   |
| Autopilot | Purple    |
| Error     | Red       |
| Normal    | Green     |
| Pause     | Yellow    |
| Recording | Blue      |
| Standby   | Cyan      |
| Other     | Off       |
