# 🚁 Drone Swarm

> A Python SDK and collection of examples for controlling DJI Ryze Tello drones individually or as a swarm.

# 🚁 Drone Swarm Ground Control Station (GCS)

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.11.0-green?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.6.1-red?style=for-the-badge&logo=python&logoColor=white)](https://www.pygame.org/)

*An academic-grade, low-latency Python Ground Control Station and SDK designed for direct teleoperation, live video stream processing, mission pad navigation, and multi-agent UAV swarm orchestration.*

---

## Overview

Drone Swarm provides a Python interface for communicating with DJI Ryze Tello drones using the official UDP SDK.

### Features
- Manual keyboard control (Pygame)
- OpenCV video streaming
- Swarm control
- Mission Pad support
- Image capture
- Video recording

## Project Structure

```text
Drone_Swarm/
├── drone_swarm/
├── examples/
├── setup.py
├── requirements.txt
├── LICENSE
└── README.md
```

## Installation

```bash
git clone https://github.com/your-username/Drone_Swarm.git
cd Drone_Swarm
pip install -r requirements.txt
pip install -e .
```

## Quick Start

```python
from drone_swarm import Tello

tello = Tello()
tello.connect()
print(tello.get_battery())
tello.takeoff()
tello.land()
tello.end()
```

## 🎮 Keyboard Controls

| Key Binding | Flight Command |
| :--- | :--- |
| **T** | Takeoff |
| **L** | Land |
| **W / S** | Ascend / Descend |
| **A / D** | Yaw Left / Right |
| **Arrow Keys** | Pitch & Roll |
| **ESC** | Graceful Exit |

---
Run:

```bash
python examples/manual-control-pygame.py
```

## Swarm Example

```python
from drone_swarm import TelloSwarm

swarm = TelloSwarm.fromIps([
    "192.168.1.101",
    "192.168.1.102",
])

swarm.connect()
try:
    swarm.takeoff()
finally:
    swarm.land()
    swarm.end()
```

## Roadmap

- [x] Manual Control
- [x] Video Streaming
- [x] Swarm Support
- [x] Mission Pads
- [ ] Formation Flight


