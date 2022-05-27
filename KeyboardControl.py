import pygame  # Import pygame module
from pygame.locals import *  # Import pygame constants
from MotorControl import MotorControl  # Import MotorControl module


class CarControlTest:  # Define CarControlTest class
    def __init__(self):  # Define __init__ method
        self.motor = MotorControl()  # Create MotorControl object
        pygame.init()  # Initialize pygame module

        pygame.display.set_mode((400, 300))  # Set display size
        self.send_inst = True  # Set send_inst to True
        self.steer()  # Call steer method

    def steer(self):  # Define steer method
        complex_cmd = False  # Set complex_cmd to False

        while self.send_inst:
            for event in pygame.event.get():
                if (event.type == KEYDOWN) or (complex_cmd):  # If key is pressed or complex_cmd is True
                    key_input = pygame.key.get_pressed()  # Get key input
                    complex_cmd = False  # Set complex_cmd to False

                    if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:  # If UP and RIGHT keys are pressed
                        print("Run Right")  # Print "Run Right"
                        complex_cmd = True  # Set complex_cmd to True

                    elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:  # If UP and LEFT keys are pressed
                        print("Run left")  # Print "Run left"
                        complex_cmd = True  # Set complex_cmd to True

                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:  # If DOWN and RIGHT keys are pressed
                        print("Back Right")  # Print "Back Right"
                        complex_cmd = True  # Set complex_cmd to True

                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:  # If DOWN and LEFT keys are pressed
                        print("Back Left")  # Print "Back Left"
                        complex_cmd = True  # Set complex_cmd to True

                    elif key_input[pygame.K_UP]:  # If UP key is pressed
                        print("Run")  # Print "Run"
                        self.motor.forward()  # Call forward method

                    elif key_input[pygame.K_DOWN]:  # If DOWN key is pressed
                        print("Back")  # Print "Back"
                        self.motor.backward()  # Call backward method

                    elif key_input[pygame.K_RIGHT]:  # If RIGHT key is pressed
                        print("Right")  # Print "Right"
                        self.motor.turn_right()  # Call turn_right method

                    elif key_input[pygame.K_LEFT]:  # If LEFT key is pressed
                        print("Left")  # Print "Left"
                        self.motor.turn_left()  # Call turn_left method

                    elif key_input[pygame.K_x] or key_input[pygame.K_q]:  # If X or Q keys are pressed
                        break  # Break loop

                elif event.type == pygame.KEYUP:  # If key is released
                    self.motor.stop()  # Call stop method

                elif event.type == pygame.QUIT:  # If window is closed
                    self.motor.stop()  # Call stop method
                    break  # Break loop


if __name__ == "__main__":  # If script is run as main
    CarControlTest()  # Call CarControlTest method
