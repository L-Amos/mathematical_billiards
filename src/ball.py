from src import utils
import numpy as np

class Ball:
    """Class representing billiards ball.

        Attributes
        ----------
        init_pos: array
            Array of initial [x, y] position.
        pos: array
            Array of current [x, y] position.
        angle: float
            Angle at which ball is initially hit.
        vel: float
            Current velocity of ball.
    """
    def __init__(self, table):
        """Creates ball instance.

        Parameters
        ----------
        table : Table class instance
            Table class instance on which the ball is placed.
        """
        while True:
            x = utils.input_test("Enter starting x position: ", integer=False)
            y = utils.input_test("Enter starting y position: ", integer=False)
            if table.geometry == "rectangle":
                if abs(x) <= table.dims[0]/2 and abs(y) <= table.dims[1]/2:
                    break
            elif table.geometry == "elliptical":
                if (x/table.dims[0])**2 + (y/table.dims[1])**2 <= 1:
                    break
            else:
                if abs(x) <= table.dims[0]/2 and abs(y) <= table.dims[1]/2:
                    if not ((x > table.dims[0]/2 and x-table.dims[0]/2 > np.sqrt((table.dims[1]/2)**2-y**2)) or (x < table.dims[0]/2 and x+table.dims[0]/2 < -np.sqrt((table.dims[1]/2)**2-y**2))):
                        break
            print('Error: not on the table')
        self.init_pos = np.array([x, y])  # Needed for plotting
        self.pos = self.init_pos
        self.angle = utils.input_test("Enter starting angle in degrees: ", integer=False)
        self.vel = [np.cos(np.radians(self.angle)), np.sin(np.radians(self.angle))]