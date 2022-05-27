from AMSpi import AMSpi as AMSpi


class MotorControl:  # MotorControl class
    def __init__(self):  # Initialize the class
        self.amspi = AMSpi()  # Initialize AMSpi class
        self.amspi.set_74HC595_pins(21, 20, 16)  # Set the pins for the 74HC595
        self.amspi.set_L293D_pins(5, 6, 13, 19)  # Set the pins for the L293D

    def backward(self, speed=100):  # Backward function
        self.amspi.run_dc_motors(  # Run the motors
            [self.amspi.DC_Motor_1, self.amspi.DC_Motor_2, self.amspi.DC_Motor_3, self.amspi.DC_Motor_4],
            speed=speed)  # Run the motors

    def stop(self):  # Stop function
        self.amspi.stop_dc_motors(
            [self.amspi.DC_Motor_1, self.amspi.DC_Motor_2, self.amspi.DC_Motor_3,
             self.amspi.DC_Motor_4])  # Stop the motors

    def forward(self, speed=100):  # Forward function
        self.amspi.run_dc_motors(
            [self.amspi.DC_Motor_1, self.amspi.DC_Motor_2, self.amspi.DC_Motor_3, self.amspi.DC_Motor_4],
            clockwise=False, speed=speed)  # Run the motors

    def turn_left(self, speed=100):  # Turn left function
        self.amspi.run_dc_motors([self.amspi.DC_Motor_1, self.amspi.DC_Motor_3], speed=speed)  # Run the motors
        self.amspi.run_dc_motors([self.amspi.DC_Motor_2, self.amspi.DC_Motor_4], clockwise=False,
                                 speed=speed)  # Run the motors

    def turn_right(self, speed=100):  # Turn right function
        self.amspi.run_dc_motors([self.amspi.DC_Motor_1, self.amspi.DC_Motor_3], clockwise=False,
                                 speed=speed)  # Run the motors
        self.amspi.run_dc_motors([self.amspi.DC_Motor_2, self.amspi.DC_Motor_4], speed=speed)  # Run the motors
