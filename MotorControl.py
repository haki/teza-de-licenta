from AMSpi import AMSpi


class MotorControl:
    def __init__(self):
        self.amspi = AMSpi()
        self.amspi.set_74HC595_pins(21, 20, 16)
        self.amspi.set_L293D_pins(5, 6, 13, 19)

    def backward(self, speed=100):
        self.amspi.run_dc_motors(
            [self.amspi.DC_Motor_1, self.amspi.DC_Motor_2, self.amspi.DC_Motor_3, self.amspi.DC_Motor_4], speed=speed)

    def stop(self):
        self.amspi.stop_dc_motors(
            [self.amspi.DC_Motor_1, self.amspi.DC_Motor_2, self.amspi.DC_Motor_3, self.amspi.DC_Motor_4])

    def forward(self, speed=100):
        self.amspi.run_dc_motors(
            [self.amspi.DC_Motor_1, self.amspi.DC_Motor_2, self.amspi.DC_Motor_3, self.amspi.DC_Motor_4],
            clockwise=False, speed=speed)

    def turn_left(self, speed=100):
        self.amspi.run_dc_motors([self.amspi.DC_Motor_1, self.amspi.DC_Motor_3], speed=speed)
        self.amspi.run_dc_motors([self.amspi.DC_Motor_2, self.amspi.DC_Motor_4], clockwise=False, speed=speed)

    def turn_right(self, speed=100):
        self.amspi.run_dc_motors([self.amspi.DC_Motor_1, self.amspi.DC_Motor_3], clockwise=False, speed=speed)
        self.amspi.run_dc_motors([self.amspi.DC_Motor_2, self.amspi.DC_Motor_4], speed=speed)
