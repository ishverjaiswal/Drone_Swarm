"""Simple example demonstrating basic autonomous flight commands using the drone_swarm SDK.

Flight Sequence:
    1. Connect to Tello and check battery percentage.
    2. Take off to hover altitude.
    3. Execute direct movement vector: Left 100cm -> Rotate 90° clockwise -> Forward 100cm.
    4. Land safely and deallocate resources.
"""

from drone_swarm import Tello


def main() -> None:
    # Initialize and connect Tello instance
    tello: Tello = Tello()
    tello.connect()

    # Check battery status before takeoff
    battery: int = tello.get_battery()
    print(f"[STATUS] Initial Battery Level: {battery}%")

    if battery < 20:
        print("[WARNING] Battery level too low to fly safely (< 20%). Aborting flight.")
        tello.end()
        return

    try:
        print("[COMMAND] Taking off...")
        tello.takeoff()

        print("[COMMAND] Moving left 100cm...")
        tello.move_left(100)

        print("[COMMAND] Rotating 90° clockwise...")
        tello.rotate_clockwise(90)

        print("[COMMAND] Moving forward 100cm...")
        tello.move_forward(100)

    finally:
        # Guarantee safe landing and socket resource release
        print("[SHUTDOWN] Landing drone and deallocating resources...")
        tello.land()
        tello.end()


if __name__ == "__main__":
    main()