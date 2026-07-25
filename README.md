# Drone Control System

A Python-based drone control library that enables communication with DJI Tello drones using the official SDK. The project provides an easy-to-use interface for controlling drone movement, receiving telemetry data, accessing the live video stream, and managing multiple drones simultaneously.

## Features

- Full support for DJI Tello SDK commands
- Real-time drone control
- Live video streaming
- Flight status and telemetry monitoring
- Multi-drone (swarm) control
- Simple and well-structured Python API
- Compatible with Python 3.6 and above

## Installation

```bash
pip install djitellopy
```

Or clone the project and install locally:

```bash
git clone <your-repository-url>
cd <your-project-folder>
pip install -e .
```

## Quick Example

```python
from djitellopy import Tello

drone = Tello()

drone.connect()
drone.takeoff()

drone.move_forward(100)
drone.rotate_clockwise(90)

drone.land()
```

## Capabilities

- Drone takeoff and landing
- Directional movement and rotation
- Video streaming
- Battery and flight information
- Multi-drone coordination
- Mission-based flight operations

## Requirements

- Python 3.6+
- DJI Tello or Tello EDU
- Wi-Fi connection to the drone

