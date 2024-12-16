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
    def __init__(self, table, x, y, angle):
        """Creates ball instance.

        Parameters
        ----------
        table : Table class instance
            Table class instance on which the ball is placed.
        """
        self.init_pos = np.array([x, y])  # Needed for plotting
        self.pos = self.init_pos
        self.angle = angle
        self.vel = [np.cos(np.radians(self.angle)), np.sin(np.radians(self.angle))]