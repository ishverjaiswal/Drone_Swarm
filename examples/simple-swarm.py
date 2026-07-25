"""Example demonstrating synchronized multi-UAV swarm control using TelloSwarm.

Swarm Operations:
    1. Connect to a fleet of drones via static IP addresses on the local router subnet.
    2. Check battery levels for every drone prior to takeoff.
    3. Perform synchronized parallel ascent (`move_up`).
    4. Execute sequential offset movements (`sequential`).
    5. Execute unique parallel movements (`parallel`).
    6. Land all drones and close UDP socket connections cleanly.
"""

import time
from typing import List
from drone_swarm import TelloSwarm

# Defined IP addresses assigned to each Tello agent on your local router subnet
SWARM_IPS: List[str] = [
    "192.168.178.42",
    "192.168.178.43",
    "192.168.178.44",
]


def main() -> None:
    print(f"[SWARM] Initializing Tello Swarm across {len(SWARM_IPS)} agents...")
    swarm: TelloSwarm = TelloSwarm.fromIps(SWARM_IPS)

    # Establish connections across all agents
    swarm.connect()
    time.sleep(1.0)  # Allow UDP socket buffers to stabilize

    # Check battery levels for all connected drones
    batteries = swarm.get_battery()
    print(f"[STATUS] Swarm Battery Levels: {batteries}")

    # Verify that every drone in the swarm has sufficient charge (> 20%)
    if any(battery < 20 for battery in batteries.values()):
        print("[WARNING] Low battery detected on one or more drones! Aborting swarm flight.")
        swarm.end()
        return

    try:
        print("[COMMAND] Swarm takeoff initiated...")
        swarm.takeoff()

        # Synchronized parallel movement: All drones move up simultaneously
        print("[COMMAND] Executing parallel ascent (100cm)...")
        swarm.move_up(100)

        # Sequential execution: Drones execute commands one after another with offset distance
        print("[COMMAND] Executing sequential forward maneuvers...")
        swarm.sequential(lambda i, tello: tello.move_forward(i * 20 + 20))

        # Parallel execution: Each drone executes a unique action simultaneously based on index
        print("[COMMAND] Executing unique parallel left maneuvers...")
        swarm.parallel(lambda i, tello: tello.move_left(i * 100 + 20))

    finally:
        # Guarantee safe landing and resource deallocation for all agents
        print("[SHUTDOWN] Landing all swarm agents and closing socket connections...")
        swarm.land()
        swarm.end()


if __name__ == "__main__":
    main()