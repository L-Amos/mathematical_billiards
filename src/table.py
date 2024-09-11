import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.patches import Rectangle
from scipy import integrate
from src import utils

class Table:
    def __init__(self, geometry):
        self.geometry = geometry
        self.reflections = 0
        self.collisions = []
        self.phase_space = []
        if self.geometry == "rectangle":
            width = utils.input_test("Table width (positive integer): ", positive=True)
            height = utils.input_test("Table height (positive integer): ", positive=True)
            self.dims = np.array([width, height])
        elif self.geometry == "elliptical":
            while True:
                a = utils.input_test("Table semi-major axis (positive integer): ", positive=True)
                b = utils.input_test("Table sami-minor axis (positive integer): ", positive=True)
                if a >= b:
                    break    
                print("Error: semi-major axis must be larger than semi-minor axis. ")
            self.dims = np.array([a, b])
        else:
            width = utils.input_test("Central width (positive integer): ", positive=True)
            height = utils.input_test("Central height (positive integer): ", positive=True)
            self.dims = np.array([width, height])

    
    def rectangle_calc(self, ball):
        width, height = self.dims
        # Collision Detection
        collisions_x = [ball.pos[0]]
        collisions_y = [ball.pos[1]]
        max_t = np.sqrt(width**2+height**2)  # Maximum amount of time it would take for a collision to occur
        t = np.arange(0, 1.1*max_t, 1e-3)
        for i in range(self.reflections):
            x_test = ball.pos[0] + ball.vel[0]*t
            y_test = ball.pos[1] + ball.vel[1]*t

            # Test for collisions with sides
            coll_x = np.where(x_test <= -width/2)[0]  # Check if gone past left side
            if not np.any(coll_x):  # If not left side, try right side
                coll_x = np.where(x_test >= width/2)[0]
                if not np.any(coll_x):  # If not, no x collision
                    coll_x = [100000]
            coll_x = coll_x[0]  # Pick first place this occurs
            
            # Test for collisions with top and bottom
            coll_y = np.where(y_test <= -height/2)[0]  # Check if gone past bottom
            if not np.any(coll_y):  # If not bottom, try top
                coll_y = np.where(y_test >= height/2)[0]
                if not np.any(coll_y):  # If not, no y collision
                    coll_y = [100000]
            coll_y = coll_y[0]  # Pick the first place this occurs
            coll_index = min(coll_x, coll_y)  # Collision index is wherever it collided first 
            
            # Change Velocity
            if coll_index == coll_x:
                ball.vel[0] = -ball.vel[0]  # If collided with a side, x-velocity changes direction
            else:
                ball.vel[1] = -ball.vel[1]  # Otherwise, y-velocity changes direction
            
            x_coll = x_test[coll_index]
            y_coll = y_test[coll_index]
            collisions_x.append(x_coll)
            collisions_y.append(y_coll)
            ball.pos = [x_coll, y_coll]  # New position is x and y coordinates of the collision with the boundary
        
        self.collisions = [collisions_x, collisions_y]

    def elliptical_calc(self, ball, phase=True):
        a, b = self.dims
        # Collision Detection
        collisions_x = [ball.pos[0]]
        collisions_y = [ball.pos[1]]
        phase_space_x = []  # Boundary perimeter from right-most point to collision
        phase_space_y = []  # Cosine of angle to tangent
        max_t = 2*a  # Maximum amount of time it would take for a collision to occur
        t = np.arange(0, 1.1*max_t, 1e-3)
        for i in range(self.reflections):
            x_test = ball.pos[0] + ball.vel[0]*t
            y_test = ball.pos[1] + ball.vel[1]*t
            f = np.round((x_test/a)**2 + (y_test/b)**2 - 1, 2)  # Equation of ellipse 
            f = f[1:]  # Remove first instance, which for any collision is where it's already colliding
            coll_index = np.where(f>=0)[0][0]  # The first index where it hits the boundary is zero
            x_coll = x_test[coll_index]
            y_coll = y_test[coll_index]
            collisions_x.append(x_coll)
            collisions_y.append(y_coll)
            ball.pos = [x_coll, y_coll]  # Update ball's position
            
            # Change Velocity
            diff_x = 2*ball.pos[0]/(a**2)
            diff_y = 2*ball.pos[1]/(b**2)
            norm_vec = [diff_x, diff_y]/np.sqrt(diff_x**2 + diff_y**2)  # Normal unit vector
            tang_vec = [-diff_y, diff_x]/np.sqrt(diff_x**2 + diff_y**2)  # Tangent unit vector
            ball.vel = -1*np.dot(ball.vel, norm_vec)*norm_vec + np.dot(ball.vel, tang_vec)*tang_vec 
        
            # Find perimeter from right-most point to collision
            elliptical_angle = np.arctan((a*ball.pos[1])/(b*ball.pos[0]))
            if elliptical_angle < 0:
                elliptical_angle += np.pi
            if phase:
                s = integrate.quad(utils.arc_length, 0, elliptical_angle, args=(a, b))[0]  # Arc length 
                phase_space_x.append(s)
                cos_alpha = np.dot(ball.vel, tang_vec)/(np.linalg.norm(ball.vel))  # Cosine of tangent angle
                phase_space_y.append(cos_alpha)
                self.phase_space = [phase_space_x, phase_space_y]
            self.collisions = [collisions_x, collisions_y]

    def stadium_calc(self, ball):
        

    def plot(self, ball, animate=True):
        if self.phase_space:
            fig, (ax, ax2) = plt.subplots(2, 1)
            ax2.set_title(f"Phase Space")
            ax2.scatter(self.phase_space[0], self.phase_space[1])
            ax2.set_xlabel("$s$")
            ax2.set_ylabel(r"$\cos{\theta}$")
            ax2.set_aspect("equal")
        else:
            fig, ax = plt.subplots()
        if self.geometry == "rectangle":
            ax.add_patch(Rectangle((-self.dims[0]/2, -self.dims[1]/2), self.dims[0], self.dims[1], fill=False, edgecolor='black', lw=3))  # Draw billiards table
            ax.set_xlim([1.1*-self.dims[0]/2, 1.1*self.dims[0]/2])
            ax.set_ylim([1.1*-self.dims[1]/2, 1.1*self.dims[1]/2])
        elif self.geometry == "elliptical":
            theta = np.linspace(0, 2*np.pi, 100)
            x = self.dims[0]*np.cos(theta)
            y=self.dims[1]*np.sin(theta)
            ax.plot(x, y, color="k")
            ax.set_xlim([1.1*-self.dims[0], 1.1*self.dims[0]])
            ax.set_ylim([1.1*-self.dims[1], 1.1*self.dims[1]])
            ax2.set_ylim([-1, 1])

        line, = ax.plot(self.collisions[0], self.collisions[1])
        if animate:
            ani = animation.FuncAnimation(fig, utils.update, len(self.collisions[0]), interval= 50*100/self.reflections, fargs=[self.collisions[0], self.collisions[1], line], blit=True, repeat=False)
        ax.scatter(ball.init_pos[0], ball.init_pos[1], marker='o', s=50, color="r", zorder=3, label="Initial Position")  # Plot starting position
        # Plot Styling & Titles
        ax.set_title(f"Trajectories of a Mathematical Billiard Ball\n in a {self.geometry.title()} Geometry ({self.reflections} Collisions)")
        ax.set_xlabel("$x$ Position")
        ax.set_ylabel("$y$ Position")
        fig.set_facecolor('lightgrey')
        ax.legend()
        plt.show()