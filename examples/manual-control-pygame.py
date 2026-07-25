import sys
import cv2
import pygame
import numpy as np
from drone_swarm import Tello

# Base movement velocity bounded between 10 and 100
DRONE_SPEED: int = 60

# Target frame rate for the Pygame window display
FRAME_RATE: int = 120


class FrontEnd:
    """Main class that handles Pygame display, Tello camera feed rendering,
    and manual keyboard teleoperation.

    Controls:
        - T: Takeoff
        - L: Land
        - Arrow keys: Forward, backward, left, and right movement
        - A / D: Counter-clockwise / clockwise yaw rotation
        - W / S: Ascend / descend altitude
        - ESC: Quit application
    """

    def __init__(self) -> None:
        # Initialize Pygame subsystems
        pygame.init()

        # Create display window and frame rate clock
        pygame.display.set_caption("Tello Live Stream - Ground Control Station")
        self.screen: pygame.Surface = pygame.display.set_mode([960, 720])
        self.clock: pygame.time.Clock = pygame.time.Clock()

        # Initialize Tello drone instance
        self.tello: Tello = Tello()

        # Directional velocities bounded between -100 and 100
        self.for_back_velocity: int = 0
        self.left_right_velocity: int = 0
        self.up_down_velocity: int = 0
        self.yaw_velocity: int = 0
        self.speed: int = 10

        self.send_rc_control: bool = False

        # Set Pygame user event timer for sending RC control vectors
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // FRAME_RATE)

    def run(self) -> None:
        # Connect to drone and set internal speed
        self.tello.connect()
        self.tello.set_speed(self.speed)

        # Check battery level upon startup
        battery: int = self.tello.get_battery()
        print(f"[STATUS] Connected to Tello. Initial Battery Level: {battery}%")
        if battery < 20:
            print("[WARNING] Low battery! Please land or recharge soon.")

        # Re-initialize camera stream cleanly
        self.tello.streamoff()
        self.tello.streamon()

        frame_read = self.tello.get_frame_read()

        try:
            should_stop: bool = False
            while not should_stop:
                for event in pygame.event.get():
                    if event.type == pygame.USEREVENT + 1:
                        self.update()
                    elif event.type == pygame.QUIT:
                        should_stop = True
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            should_stop = True
                        else:
                            self.keydown(event.key)
                    elif event.type == pygame.KEYUP:
                        self.keyup(event.key)

                if frame_read.stopped:
                    break

                self.screen.fill([0, 0, 0])

                # Retrieve latest frame from Tello camera and verify existence
                frame = frame_read.frame
                if frame is None:
                    self.clock.tick(FRAME_RATE)
                    continue

                # Overlay battery telemetry on the live video stream
                text: str = f"Battery: {self.tello.get_battery()}%"
                cv2.putText(
                    frame,
                    text,
                    (15, 720 - 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                )

                # Convert OpenCV frame format (BGR) to Pygame surface format (RGB)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = np.rot90(frame)
                frame = np.flipud(frame)

                # Render frame onto Pygame display
                frame_surface: pygame.Surface = pygame.surfarray.make_surface(frame)
                self.screen.blit(frame_surface, (0, 0))
                pygame.display.update()

                # Maintain stable target frame rate
                self.clock.tick(FRAME_RATE)

        finally:
            # Deallocate camera feed and gracefully shut down
            print("[SHUTDOWN] Releasing drone resources and closing window...")
            self.tello.end()
            pygame.quit()

    def keydown(self, key: int) -> None:
        """Update velocity variables on key press events."""
        if key == pygame.K_UP:          # Pitch Forward
            self.for_back_velocity = DRONE_SPEED
        elif key == pygame.K_DOWN:      # Pitch Backward
            self.for_back_velocity = -DRONE_SPEED
        elif key == pygame.K_LEFT:      # Roll Left
            self.left_right_velocity = -DRONE_SPEED
        elif key == pygame.K_RIGHT:     # Roll Right
            self.left_right_velocity = DRONE_SPEED
        elif key == pygame.K_w:         # Ascend
            self.up_down_velocity = DRONE_SPEED
        elif key == pygame.K_s:         # Descend
            self.up_down_velocity = -DRONE_SPEED
        elif key == pygame.K_a:         # Yaw Counter-Clockwise
            self.yaw_velocity = -DRONE_SPEED
        elif key == pygame.K_d:         # Yaw Clockwise
            self.yaw_velocity = DRONE_SPEED

    def keyup(self, key: int) -> None:
        """Reset velocity variables or execute command triggers on key release events."""
        if key in (pygame.K_UP, pygame.K_DOWN):
            self.for_back_velocity = 0
        elif key in (pygame.K_LEFT, pygame.K_RIGHT):
            self.left_right_velocity = 0
        elif key in (pygame.K_w, pygame.K_s):
            self.up_down_velocity = 0
        elif key in (pygame.K_a, pygame.K_d):
            self.yaw_velocity = 0
        elif key == pygame.K_t:         # Trigger Takeoff
            print("[COMMAND] Takeoff initiated")
            self.tello.takeoff()
            self.send_rc_control = True
        elif key == pygame.K_l:         # Trigger Landing
            print("[COMMAND] Landing initiated")
            self.tello.land()
            self.send_rc_control = False

    def update(self) -> None:
        """Send directional RC control vectors to Tello via UDP socket."""
        if self.send_rc_control:
            self.tello.send_rc_control(
                self.left_right_velocity,
                self.for_back_velocity,
                self.up_down_velocity,
                self.yaw_velocity,
            )


def main() -> None:
    frontend = FrontEnd()
    frontend.run()


if __name__ == "__main__":
    main()