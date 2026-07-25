"""Example demonstrating Tello Mission Pad detection and autonomous reaction logic.

Flight Logic:
    - Enables mission pad detection (forward camera mode).
    - Checks for Mission Pad IDs in a loop:
        - If Pad 3 is detected: Move backward 30cm and rotate 90° clockwise.
        - If Pad 4 is detected: Move upward 30cm and execute a forward flip.
    - Terminates and lands when Pad 1 is detected or max iterations are reached.
"""

import time
from drone_swarm import Tello

MAX_DETECTION_ATTEMPTS: int = 100


def main() -> None:
    # Initialize and connect Tello instance
    tello: Tello = Tello()
    tello.connect()

    battery: int = tello.get_battery()
    print(f"[STATUS] Initial Battery Level: {battery}%")

    if battery < 20:
        print("[WARNING] Battery level too low to fly safely (< 20%).")
        return

    # Configure mission pad detection settings
    # Detection Direction: 0 = Downward, 1 = Forward, 2 = Both
    tello.enable_mission_pads()
    tello.set_mission_pad_detection_direction(1)

    print("[COMMAND] Taking off...")
    tello.takeoff()

    try:
        attempts: int = 0
        pad_id: int = tello.get_mission_pad_id()

        print("[STATUS] Searching for Mission Pads...")
        while pad_id != 1 and attempts < MAX_DETECTION_ATTEMPTS:
            attempts += 1

            if pad_id == 3:
                print("[EVENT] Detected Pad 3: Moving back 30cm and rotating 90° clockwise.")
                tello.move_back(30)
                tello.rotate_clockwise(90)

            elif pad_id == 4:
                print("[EVENT] Detected Pad 4: Moving up 30cm and flipping forward.")
                tello.move_up(30)
                tello.flip_forward()

            # Small pause to prevent socket flooding
            time.sleep(0.2)
            pad_id = tello.get_mission_pad_id()

        if pad_id == 1:
            print("[EVENT] Detected Pad 1: Target reached successfully!")
        else:
            print("[WARNING] Max detection attempts reached without locating Pad 1.")

    finally:
        # Graceful cleanup and safe landing
        print("[SHUTDOWN] Disabling mission pads, landing, and releasing resources...")
        tello.disable_mission_pads()
        tello.land()
        tello.end()


if __name__ == "__main__":
    main()