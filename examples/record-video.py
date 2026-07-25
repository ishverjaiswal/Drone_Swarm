"""Example demonstrating background multithreaded video recording during flight operations.

Flight Sequence:
    1. Connect to Tello and start the camera stream.
    2. Spawn a background daemon thread to capture frames to 'video.avi'.
    3. Take off, climb 100cm, execute a 360° counter-clockwise rotation, and land.
    4. Safely stop video recording and release file resources.
"""

import time
import cv2
from threading import Thread
from drone_swarm import Tello

# Global flag to signal the video recording thread
keep_recording: bool = True


def video_recorder(tello: Tello) -> None:
    """Background target function to continuously write camera frames to an AVI video file."""
    global keep_recording

    frame_read = tello.get_frame_read()

    # Wait until a valid frame is received from the camera stream
    while frame_read.frame is None:
        time.sleep(0.1)

    height, width, _ = frame_read.frame.shape
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    video = cv2.VideoWriter("video.avi", fourcc, 30, (width, height))

    print("[RECORDING] Started background video recording to 'video.avi'...")
    try:
        while keep_recording:
            frame = frame_read.frame
            if frame is not None:
                video.write(frame)
            time.sleep(1 / 30)
    finally:
        print("[RECORDING] Releasing video writer...")
        video.release()


def main() -> None:
    global keep_recording

    # Initialize and connect Tello instance
    tello: Tello = Tello()
    tello.connect()

    battery: int = tello.get_battery()
    print(f"[STATUS] Initial Battery Level: {battery}%")

    if battery < 20:
        print("[WARNING] Battery level too low to fly safely (< 20%).")
        return

    # Start video stream
    tello.streamoff()
    tello.streamon()

    # Launch recorder in a dedicated thread to prevent blocking flight commands
    recorder: Thread = Thread(target=video_recorder, args=(tello,))
    recorder.start()

    try:
        print("[COMMAND] Taking off...")
        tello.takeoff()

        print("[COMMAND] Ascending 100cm...")
        tello.move_up(100)

        print("[COMMAND] Executing 360° counter-clockwise rotation...")
        tello.rotate_counter_clockwise(360)

    finally:
        print("[SHUTDOWN] Landing drone and stopping recorder...")
        tello.land()

        # Signal thread termination and wait for thread exit
        keep_recording = False
        recorder.join()

        # Clean up SDK resources
        tello.streamoff()
        tello.end()
        print("[SHUTDOWN] Flight and recording complete.")


if __name__ == "__main__":
    main()