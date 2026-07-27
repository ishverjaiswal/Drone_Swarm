# 🚁 Drone Swarm Ground Control Station (GCS)

> A Full-Stack Ground Control Station (GCS) for managing and monitoring multiple **DJI Tello EDU** drones in real time using **Python**, **FastAPI**, **React**, **WebSockets**, and **OpenCV**.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-Frontend-61DAFB)
![WebSocket](https://img.shields.io/badge/WebSocket-Real--Time-orange)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

# 📖 Overview

Drone Swarm Ground Control Station (GCS) is a **full-stack drone management platform** built on top of the DJI Tello SDK.

Unlike traditional example scripts that only send flight commands, this project provides a complete monitoring and management system capable of:

* Monitoring multiple drones simultaneously
* Displaying live telemetry
* Streaming real-time updates through WebSockets
* Persisting telemetry into a database
* Providing a modern React-based Ground Control Station
* Managing drone connections dynamically

The project demonstrates concepts commonly found in professional UAV software such as Mission Planner, QGroundControl, and enterprise fleet monitoring systems.

---

# 🎯 Objectives

The primary goal of this project is to demonstrate how modern software engineering principles can be applied to drone systems by combining:

* Drone Networking
* Backend Development
* Frontend Development
* Database Management
* Real-Time Communication
* Computer Vision
* Software Architecture

---

# ✨ Features

## 🚁 Drone Control

* Connect to DJI Tello EDU drones
* Takeoff / Land
* Emergency Stop
* Manual Flight Control
* Velocity Control
* RC Commands
* Keyboard Control
* Multi-drone Control

---

## 📡 Real-Time Telemetry

Display live drone information including:

* Battery Percentage
* Height
* Temperature
* Flight Time
* Speed
* Pitch
* Roll
* Yaw
* Time of Flight (ToF)
* IMU State
* Flight Status

Telemetry updates continuously without refreshing the page.

---

## 🌐 Ground Control Station

Modern web dashboard built using React.

Features include:

* Live Drone Status
* Active Drone List
* Drone Health Monitoring
* Battery Indicators
* Telemetry Cards
* Live Charts
* Connection Status
* Real-Time Updates

---

## 🔄 WebSocket Communication

Instead of polling the backend repeatedly, telemetry is pushed instantly using WebSockets.

Benefits:

* Low latency
* Real-time dashboard
* Reduced network overhead
* Scalable architecture

---

## 💾 Database Integration

Telemetry is stored using SQLite and SQLAlchemy.

Possible use cases:

* Flight history
* Telemetry replay
* Analytics
* Debugging
* Future reporting system

---

## 📹 Video Streaming

Supports:

* Live Camera Feed
* OpenCV Integration
* Image Capture
* Video Recording

---

## 👥 Swarm Management

Supports managing multiple DJI Tello EDU drones.

Features include:

* Multiple Drone Connections
* Dynamic Drone Registration
* Drone Identification
* Parallel Commands
* Sequential Commands

---

## 🎮 Manual Control

Keyboard based flight controller using Pygame.

Supports:

* Takeoff
* Landing
* Movement
* Camera Stream

---

## 🧩 Modular SDK

The project is organized as a reusable Python SDK.

Example applications are separated from the core communication layer.

---

# 🏗️ System Architecture

```
                    User

                      │

             React Dashboard

                      │

              WebSocket Client

                      │

                FastAPI Backend

      ┌───────────────┼───────────────┐
      │               │               │
Telemetry API   Database Layer   WebSocket Server

                      │

              Drone Swarm SDK

                      │

          UDP Socket Communication

                      │

         DJI Tello EDU Drone(s)
```

---

# 📂 Project Structure

```
Drone-Swarm-GCS/

│
├── drone_swarm/
│   ├── tello.py
│   ├── tello_swarm.py
│   ├── swarm.py
│   └── utils.py
│
├── examples/
│   ├── keyboard_control.py
│   ├── manual_control.py
│   ├── video_stream.py
│   ├── image_capture.py
│   ├── mission_pad.py
│   └── swarm_demo.py
│
├── dashboard/
│   ├── backend/
│   │     ├── main.py
│   │     ├── database.py
│   │     ├── models.py
│   │     └── websocket.py
│   │
│   └── frontend/
│         ├── src/
│         ├── components/
│         └── pages/
│
├── telemetry.db
├── requirements.txt
└── README.md
```

---

# ⚙️ Technology Stack

## Backend

* Python
* FastAPI
* SQLAlchemy
* SQLite
* WebSockets
* Uvicorn

---

## Frontend

* React
* JavaScript
* HTML
* CSS

---

## Drone Communication

* DJI Tello SDK
* UDP Socket Programming
* Real-Time Networking

---

## Computer Vision

* OpenCV
* NumPy

---

## Desktop Interface

* Pygame

---

# 🔄 Communication Flow

```
DJI Tello

↓

UDP State Packets

↓

Drone SDK

↓

Telemetry Parser

↓

FastAPI Backend

↓

WebSocket Server

↓

React Dashboard

↓

User
```

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/ishverjaiswal/Drone_Swarm/

cd drone-swarm-gcs
```

---

## Install Backend

```bash
pip install -r requirements.txt
```

---

## Start Backend

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## Install Frontend

```bash
cd dashboard/frontend

npm install
```

---

## Run Frontend

```bash
npm start
```

---

# 📊 Dashboard Features

The Ground Control Station provides:

* Drone Overview
* Live Telemetry
* Battery Monitoring
* Flight Status
* Connection Status
* Active Drone Counter
* Real-Time Charts
* Swarm Monitoring

---

# 🛰️ Supported Drone Operations

* Connect
* Disconnect
* Takeoff
* Land
* Emergency Stop
* Move Up
* Move Down
* Move Left
* Move Right
* Video Stream


---

# 📈 Future Improvements

Planned enhancements include:

* GPS Visualization
* Flight Path Recording
* YOLO-Based Object Detection
* Authentication
* Cloud Telemetry Storage
* ArduPilot/PX4 Support
* Flight Log Export (CSV/PDF)

---

# 🧪 Testing

Future improvements include:

* Unit Tests
* Integration Tests
* API Tests
* Load Testing
* Continuous Integration

---

# 📚 What I Learned

This project helped me gain practical experience in:

* Python Package Development
* UDP Socket Programming
* FastAPI
* React
* SQLAlchemy
* SQLite
* WebSockets
* OpenCV
* Pygame
* Object-Oriented Programming
* Software Architecture
* Full-Stack Development

---

# 📌 Limitations

* Currently supports DJI Tello/Tello EDU drones.
* GPS-based navigation is not available because Tello drones do not include GPS hardware.
* Swarm functionality depends on proper Wi-Fi network configuration.
* Mission planning is currently limited to supported Tello SDK commands.

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push the branch.
5. Open a Pull Request.

---

# 📄 License

This project is released under the MIT License.

---

# 🙏 Acknowledgements

This project builds upon the capabilities provided by the **DJI Tello SDK** and extends them with a full-stack Ground Control Station, real-time telemetry streaming, database integration, and a modern web interface for educational and research purposes.

---

# ⭐ If You Like This Project

If you found this project useful, please consider giving it a ⭐ on GitHub.

It helps others discover the project and supports future development.
