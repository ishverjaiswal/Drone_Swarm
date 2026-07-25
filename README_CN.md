# DJITelloPy

DJITelloPy is a Python interface for DJI Tello drones built on the official Tello SDK and Tello EDU SDK. It provides a simple way to communicate with and control Tello drones using Python.

## Features

- Support for all DJI Tello SDK commands
- Live video streaming
- Real-time drone state and telemetry
- Multi-drone (swarm) control
- Compatible with Python 3.6 and above

## Installation

Install using pip:

```bash
pip install djitellopy
```

On Linux systems with both Python 2 and Python 3 installed, use:

```bash
pip3 install djitellopy
```

## Developer Installation

Clone the repository and install it in editable mode:

```bash
git clone https://github.com/damiafuentes/DJITelloPy.git
cd DJITelloPy
pip install -e .
```

## Usage

### Basic Example

```python
from djitellopy import Tello

tello = Tello()

tello.connect()
tello.takeoff()

tello.move_left(100)
tello.rotate_counter_clockwise(90)
tello.move_forward(100)

tello.land()
```

## Example Programs

The project includes several example scripts:

- Capture photos
- Record videos
- Control multiple drones simultaneously
- Keyboard-based manual control
- Mission pad detection
- Pygame-based manual control

## Notes

- If the `streamon` command returns `Unknown command`, update the drone firmware using the DJI Tello app.
- Mission pad detection is supported only on Tello EDU.
- A bright environment is recommended for reliable mission pad detection.
- Connecting to an existing Wi-Fi network is supported only on Tello EDU.
- Video streaming is unavailable when connected through an external Wi-Fi network.

