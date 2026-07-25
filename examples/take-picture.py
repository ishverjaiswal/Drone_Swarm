"""Example demonstrating autonomous takeoff, still-image capture via OpenCV, and safe landing.

Sequence:
    1. Connect to Tello and check initial battery level.
    2. Start video stream and wait for a valid frame buffer.
    3. Take off and save a frame to 'picture.png'.
    4. Land safely and deallocate stream resources.
"""

import time
import cv2
from drone_swarm import Tello


def main() -> None:
    # Initialize and connect Tello instance
    tello: Tello = Tello()
    tello.connect()

    # Check battery percentage
    battery: int = tello.get_battery()
    print(f"[STATUS] Initial Battery Level: {battery}%")

    if battery < 20:
        print("[WARNING] Battery level too low to fly safely (< 20%). Aborting task.")
        tello.end()
        return

    # Start video stream
    tello.streamoff()
    tello.streamon()
    frame_read = tello.get_frame_read()

    # Wait briefly for camera stream buffer to populate
    print("[STATUS] Initializing camera stream...")
    retry_count: int = 0
    while frame_read.frame is None and retry_count < 50:
        time.sleep(0.1)
        retry_count += 1

    try:
        print("[COMMAND] Taking off...")
        tello.takeoff()

        # Capture frame from live buffer
        frame = frame_read.frame
        if frame is not None:
            cv2.imwrite("picture.png", frame)
            print("[SUCCESS] Photo captured and saved to 'picture.png'.")
        else:
            print("[ERROR] Failed to capture valid frame from camera stream.")

    finally:
        # Guarantee safe landing and resource deallocation
        print("[SHUTDOWN] Landing drone and stopping camera stream...")
        tello.land()
        tello.streamoff()
        tello.end()


if __name__ == "__main__":
    main()