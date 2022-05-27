import pygame
from pygame.locals import *
from MotorControl import MotorControl


class CarControlTest:
    def __init__(self):
        self.motor = MotorControl()
        pygame.init()

        pygame.display.set_mode((400, 300))
        self.send_inst = True
        self.steer()

    def steer(self):
        complex_cmd = False

        while self.send_inst:
            for event in pygame.event.get():
                if (event.type == KEYDOWN) or (complex_cmd):
                    key_input = pygame.key.get_pressed()
                    complex_cmd = False

                    if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                        print("Run Right")
                        complex_cmd = True

                    elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                        print("Run left")
                        complex_cmd = True

                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
                        print("Back Right")
                        complex_cmd = True

                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
                        print("Back Left")
                        complex_cmd = True
                        # self.ser.write(b'8')

                    elif key_input[pygame.K_UP]:
                        print("Run")
                        self.motor.forward()

                    elif key_input[pygame.K_DOWN]:
                        print("Back")
                        self.motor.backward()

                    elif key_input[pygame.K_RIGHT]:
                        print("Right")
                        self.motor.turn_right()

                    elif key_input[pygame.K_LEFT]:
                        print("Left")
                        self.motor.turn_left()

                    elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                        break

                elif event.type == pygame.KEYUP:
                    self.motor.stop()

                elif event.type == pygame.QUIT:
                    self.motor.stop()
                    break


if __name__ == "__main__":
    CarControlTest()