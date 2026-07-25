# Drone Swarm

Drone Swarm is a Python package for controlling and coordinating multiple DJI Tello drones using the official Tello SDK. It provides a simple and extensible API for drone communication, flight control, telemetry monitoring, video streaming, and swarm coordination.

## Features

* Control DJI Tello and Tello EDU drones
* Execute autonomous flight commands
* Real-time telemetry monitoring
* Live video streaming support
* Multi-drone swarm management
* High-level Python API
* Compatible with Python 3.6 and above

---

## Project Structure

```text
Drone_Swarm/
│
├── drone_swarm/
│   ├── __init__.py
│   ├── tello.py
│   ├── swarm.py
│   └── enforce_types.py
│
├── docs/
├── examples/
├── README.md
├── requirements.txt
└── setup.py
```

---

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

Or, if the package is published to PyPI in the future:

```bash
pip install drone_swarm
```

---

## Quick Start

```python
from drone_swarm import Tello

drone = Tello()

drone.connect()

print("Battery:", drone.get_battery())

drone.takeoff()

drone.move_forward(100)
drone.rotate_clockwise(90)

drone.land()
```

---

## Swarm Example

```python
from drone_swarm import TelloSwarm

swarm = TelloSwarm.fromIps([
    "192.168.10.1",
    "192.168.10.2"
])

swarm.connect()
swarm.takeoff()

swarm.parallel(lambda index, tello: tello.move_up(50))

swarm.land()
```

---

## Capabilities

* Drone connection management
* Flight control
* Telemetry monitoring
* Battery status
* Video streaming
* Swarm coordination
* Mission execution
* Emergency stop support

---

## Requirements

* Python 3.6+
* DJI Tello or Tello EDU
* Wi-Fi connection to the drone

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## Repository

GitHub:

```
https://github.com/ishverjaiswal/Drone_Swarm
```



