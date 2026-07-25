"""Simple example demonstrating real-time keyboard control of a Tello drone using OpenCV.

For a fully featured Pygame GUI example, see manual-control-pygame.py.

Controls:
    - W / S: Move Forward / Backward
    - A / D: Move Left / Right
    - R / F: Ascend / Descend
    - E / Q: Yaw Rotate Clockwise / Counter-Clockwise
    - ESC: Land drone and exit program
"""

import cv2
from drone_swarm import Tello

# Base movement velocity bounded between 10 and 100
SPEED: int = 50


def main() -> None:
    tello: Tello = Tello()
    tello.connect()

    battery: int = tello.get_battery()
    print(f"[STATUS] Initial Battery Level: {battery}%")

    if battery < 20:
        print("[WARNING] Battery too low to fly safely (< 20%).")
        return

    # Initialize video stream
    tello.streamoff()
    tello.streamon()
    frame_read = tello.get_frame_read()

    # Take off
    print("[COMMAND] Taking off...")
    tello.takeoff()

    try:
        while True:
            # Retrieve current frame from thread
            img = frame_read.frame

            if img is None:
                continue

            # Overlay battery indicator on OpenCV window
            cv2.putText(
                img,
                f"Battery: {tello.get_battery()}%",
                (15, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2,
            )

            cv2.imshow("Tello Ground Control Station", img)

            # Non-blocking key capture (1ms wait)
            key: int = cv2.waitKey(1) & 0xFF

            if key == 27:  # ESC key
                print("[COMMAND] ESC pressed. Exiting...")
                break

            # Initialize direction vectors
            left_right: int = 0
            forward_backward: int = 0
            up_down: int = 0
            yaw: int = 0

            # Velocity controls
            if key == ord("w"):
                forward_backward = SPEED
            elif key == ord("s"):
                forward_backward = -SPEED
            elif key == ord("a"):
                left_right = -SPEED
            elif key == ord("d"):
                left_right = SPEED
            elif key == ord("r"):
                up_down = SPEED
            elif key == ord("f"):
                up_down = -SPEED
            elif key == ord("e"):
                yaw = SPEED
            elif key == ord("q"):
                yaw = -SPEED

            # Continuous velocity command transmission
            tello.send_rc_control(left_right, forward_backward, up_down, yaw)

    finally:
        print("[SHUTDOWN] Landing drone and releasing resources...")
        tello.send_rc_control(0, 0, 0, 0)
        tello.land()
        tello.streamoff()
        tello.end()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()