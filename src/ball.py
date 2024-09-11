from src import utils
import numpy as np

class Ball:
    def __init__(self, table):
        while True:
            x = utils.input_test("Enter starting x position: ", integer=False)
            y = utils.input_test("Enter starting y position: ", integer=False)
            if table.geometry == "rectangle":
                if abs(x) <= table.dims[0]/2 or abs(y) <= table.dims[1]/2:
                    break
            elif table.geometry == "elliptical":
                if (x/table.dims[0])**2 + (y/table.dims[1])**2 <= 1:
                    break
            print('Error: not on the table')
        self.init_pos = np.array([x, y])  # Needed for plotting
        self.pos = self.init_pos
        self.angle = utils.input_test("Enter starting angle in degrees: ", integer=False)
        self.vel = [np.cos(np.radians(self.angle)), np.sin(np.radians(self.angle))]