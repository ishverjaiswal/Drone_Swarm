# Drone Swarm

Drone Swarm is a Python package for controlling and coordinating DJI Tello and Tello EDU drones using the official Tello SDK. It provides a clean Python API for drone communication, flight control, telemetry monitoring, live video streaming, and swarm management.

## Features

* Full support for DJI Tello SDK commands
* Real-time flight control
* Live video streaming
* Drone telemetry and status monitoring
* Multi-drone swarm coordination
* Simple and extensible Python API
* Compatible with Python 3.6 and above

## Installation

Clone the repository:

```bash
git clone https://github.com/ishverjaiswal/Drone_Swarm.git
cd Drone_Swarm
```

Install the package in editable mode:

```bash
pip install -e .
```

Or, if the package is published on PyPI in the future:

```bash
pip install drone_swarm
```

## Usage

### Basic Example

```python
from drone_swarm import Tello

drone = Tello()

drone.connect()

print("Battery:", drone.get_battery())

drone.takeoff()

drone.move_left(100)
drone.rotate_counter_clockwise(90)
drone.move_forward(100)

drone.land()
```

## Swarm Example

```python
from drone_swarm import TelloSwarm

swarm = TelloSwarm.fromIps([
    "192.168.10.1",
    "192.168.10.2"
])

swarm.connect()

swarm.takeoff()

swarm.parallel(lambda index, drone: drone.move_up(50))

swarm.land()
```

## Example Programs

The repository includes example programs for:

* Basic drone control
* Image capture
* Video streaming
* Multi-drone swarm control
* Keyboard-based manual control
* Mission pad detection
* Autonomous flight operations

## Requirements

* Python 3.6+
* DJI Tello or Tello EDU
* Wi-Fi connection to the drone

Install project dependencies:

```bash
pip install -r requirements.txt
```

## Repository

GitHub:

```text
https://github.com/ishverjaiswal/Drone_Swarm
```

## Notes

* Ensure the drone firmware is up to date before use.
* Mission pad functionality is available only on Tello EDU.
* Use the drone in a well-lit environment for reliable mission pad detection.
* Live video streaming requires a stable Wi-Fi connection.
* Refer to the `examples/` directory for additional usage demonstrations.

## ⚙️ Installation

```bash
pip install drone_swarm_gcs


## 🛠️ Architecture & Acknowledgments

This Ground Control Station utilizes the core UDP socket communication protocols established by [DJITelloPy](https://github.com/damiafuentes/DJITelloPy). 

**Key Custom Enhancements Developed in this Repository:**
- **Custom Teleoperation Interface:** Built an interactive Pygame Ground Control Station with live telemetry HUD overlays.
- **Multithreaded Video Pipeline:** Implemented non-blocking background video recording and frame processing using OpenCV.
- **Enhanced Type Safety & Controls:** Integrated strict type enforcement and pre-flight battery/connection health guards.
- **Swarm Orchestration:** Configured parallel and sequential fleet command loops over local router subnets.
