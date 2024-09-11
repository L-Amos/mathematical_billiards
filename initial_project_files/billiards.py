# %matplotlib qt5
# -*- coding: utf-8 -*-
""" Mathematical Billiards

This program simulates mathematical billiards on rectangular, elliptical and Bunimovich-stadium tables.

Author:
    Luke Amos
    University of Birmingham
    Student ID: 2297692

Created on Tue Oct 17 16:39:42 2023
"""

### IMPORTS ###
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.patches import Rectangle
from scipy import integrate
from time import sleep
from sys import exit

def update(num, collisions_x, collisions_y, line):
    """Plot Update Function
    
    Needed for the animation of the Bunimovich billiards trajectory plot.
    
    Parameters
    ----------
        num: int
            serves as an incrementer
        collisions_x: 1D array
            x coordinates of collision points
        collisions_y: 1D array
            y coordinates of collision points
        line: matplotlib object
            line of the matplotlib plot
    
    Returns
    -------
        line: matplotlib object
            updated line for matplotlib plot
    """
    line.set_data(collisions_x[:num+1], collisions_y[:num+1])
    return line,

def box_geometry(pos, vel, dims, reflections):
    global ani  # Needed for animation (due to issues within Python)
    """Box Geometry Function
    
        - Draws Rectangular Boundary
        - Calculates Collisions With Boundary
        - Plots Collisions
        
    Parameters
    ----------
        pos: 1D array
            starting position of billiard ball
        vel: 1D array
            starting velocity of billiard ball
        dims: 1D array
            dimensions of billiard table in the form [width, height]
        reflections: int
            number of reflections of the ball off the boundary to calculate
    """
    width, height = dims
    fig, ax = plt.subplots()
    ax.add_patch(Rectangle((-width/2, -height/2), width, height, fill=False, edgecolor='black', lw=3))  # Draw rectangle
    # Make axes look nicer
    ax.set_xlim([1.1*-width/2, 1.1*width/2])
    ax.set_ylim([1.1*-height/2, 1.1*height/2])
    ax.set_aspect("equal")
   
    ax.scatter(pos[0], pos[1], marker='o', s=50, color="r", zorder=3, label="Initial Position")  # Plot starting position
    # Collision Detection
    collisions_x = [pos[0]]
    collisions_y = [pos[1]]
    max_t = np.sqrt(width**2+height**2)  # Maximum amount of time it would take for a collision to occur
    t = np.arange(0, 1.1*max_t, 1e-3)
    for i in range(reflections):
        x_test = pos[0] + vel[0]*t
        y_test = pos[1] + vel[1]*t

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
            vel[0] = -vel[0]  # If collided with a side, x-velocity changes direction
        else:
            vel[1] = -vel[1]  # Otherwise, y-velocity changes direction
        
        x_coll = x_test[coll_index]
        y_coll = y_test[coll_index]
        collisions_x.append(x_coll)
        collisions_y.append(y_coll)
        pos = [x_coll, y_coll]  # New position is x and y coordinates of the collision with the boundary
    
    # Animate Plot
    line, = ax.plot(collisions_x, collisions_y)
    ani = animation.FuncAnimation(fig, update, len(collisions_x), interval= 50*100/reflections, fargs=[collisions_x, collisions_y, line], blit=True, repeat=False)
    
    # Plot Styling & Titles
    ax.set_title(f"Trajectories of a Mathematical Billiard Ball\n in a Box Geometry ({reflections} Collisions)")
    ax.set_xlabel("$x$ Position")
    ax.set_ylabel("$y$ Position")
    ax.set_ylim([-0.55, 0.7])
    fig.set_facecolor('lightgrey')
    ax.legend()
    plt.show()
    

def arc_length(angle, a, b):  
    """Arc Length of Ellipse 
    
    Integrated to calculate arc length of the ellipse from right-most point to point of collision.
    
    Parameters
    ----------
        angle: float
            elliptical angle in radians 
        a: float
            semi-major axis of the ellipse
        b: float
           semi-minor axis of the ellipse
    
    Returns
    -------
        f: float
            integrand of ellpise arc length calculation
    """
    f = np.sqrt((a*np.cos(angle))**2+(b*np.sin(angle))**2)
    return f

def elliptical_geometry(pos, angle, dims, reflections, plot=True):
    global ani  # Needed for animation (due to issues within Python)
    """Elliptical Geometry Function
    
        - Draws Elliptical Boundary
        - Calculates Collisions With Boundary
        - Plots Collisions
        - Calculates + Plots Phase Space Coordinates
        
    Parameters
    ----------
        pos: 1D array
            initial position of billiard ball
        angle: float
            angle in degrees at which ball is hit
        dims: 1D array
            dimensions of ellipse in the form [semi-major axis, semi-minor axis]
        reflections: int
            number of reflections of the ball off the boundary to calculate
        plot: bool, default True
            flag for whether we want to output a plot or not
    """
    a, b = dims
    vel = [np.cos(np.radians(angle)), np.sin(np.radians(angle))]
    
    # Collision Detection
    collisions_x = [pos[0]]
    collisions_y = [pos[1]]
    phase_space_x = []  # Boundary perimeter from right-most point to collision
    phase_space_y = []  # Cosine of angle to tangent
    max_t = 2*a  # Maximum amount of time it would take for a collision to occur
    t = np.arange(0, 1.1*max_t, 1e-3)
    for i in range(reflections):
        x_test = pos[0] + vel[0]*t
        y_test = pos[1] + vel[1]*t
        f = np.round((x_test/a)**2 + (y_test/b)**2 - 1, 2)  # Equation of ellipse 
        f = f[1:]  # Remove first instance, which for any collision is where it's already colliding
        coll_index = np.where(f>=0)[0][0]  # The first index where it hits the boundary is zero
        x_coll = x_test[coll_index]
        y_coll = y_test[coll_index]
        collisions_x.append(x_coll)
        collisions_y.append(y_coll)
        pos = [x_coll, y_coll]  # Update ball's position
        
        # Change Velocity
        diff_x = 2*pos[0]/(a**2)
        diff_y = 2*pos[1]/(b**2)
        norm_vec = [diff_x, diff_y]/np.sqrt(diff_x**2 + diff_y**2)  # Normal unit vector
        tang_vec = [-diff_y, diff_x]/np.sqrt(diff_x**2 + diff_y**2)  # Tangent unit vector
        vel = -1*np.dot(vel, norm_vec)*norm_vec + np.dot(vel, tang_vec)*tang_vec 
       
        # Find perimeter from right-most point to collision
        elliptical_angle = np.arctan((a*pos[1])/(b*pos[0]))
        if elliptical_angle < 0:
            elliptical_angle += np.pi
        s = integrate.quad(arc_length, 0, elliptical_angle, args=(a, b))[0]  # Arc length 
        phase_space_x.append(s)
        cos_alpha = np.dot(vel, tang_vec)/(np.linalg.norm(vel))  # Cosine of tangent angle
        phase_space_y.append(cos_alpha)
    if plot:
        fig, (ax1, ax2) = plt.subplots(2, 1)
        
        # Draw Boundary
        theta = np.linspace(0, 2*np.pi, 100)
        x = a*np.cos(theta)
        y=b*np.sin(theta)
        ax1.plot(x, y, color="k")
        
        # Make axes look nicer
        ax1.set_xlim([1.1*-a, 1.1*a])
        ax1.set_ylim([1.1*-b, 1.1*b])
        ax1.set_aspect("equal")   
        ax2.set_aspect("equal") 
               
        # Animate Plot
        line, = ax1.plot(collisions_x, collisions_y)
        ani = animation.FuncAnimation(fig, update, len(collisions_x), interval= 50*100/reflections, fargs=[collisions_x, collisions_y, line], blit=True, repeat=False)
        
        # Plot Styling & Titles
        fig.set_facecolor('lightgrey')
        fig.suptitle(f"Elliptical Mathematical Billiards with semi-major axis $a={a}$, semi-minor axis $b={b}$\n with the ball initially at ({collisions_x[0]}, {collisions_y[0]}) and hit at an angle of $\\theta = {angle}\degree$", fontsize=16)
        ax1.set_title(f"Trajectories in Real Space ({reflections} Collisions)")
        ax1.scatter(collisions_x[0], collisions_y[0], marker='o', s=50, color="r", zorder=3, label="Initial Position")  # Plot starting position
        ax1.set_xlabel("$x$ Position")
        ax1.set_ylabel("$y$ Position")
        ax2.scatter(phase_space_x, phase_space_y)
        ax2.set_title(f"Phase Space")
        ax2.set_xlabel("$s$")
        ax2.set_ylabel(r"$\cos{\theta}$")
        ax2.set_ylim([-1, 1])
        ax2.set_xlim([0, 5])
        ax1.legend()
        plt.show()
    else:
        return(collisions_x, collisions_y, phase_space_x, phase_space_y)

def elliptical_demo():
    """Demo of Interesting Elliptical Billiards
    
    Sets up an elliptical billiards table with a=2 and b=1. Hits the ball at 45 degrees for a range of interesting starting points, and plots the results.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1)
    positions = [
        [0, 0], 
        [-1.7, 0], 
        [-1.99, 0],
        [1.99, 0],
        [0,-0.99],
        [-1.8, 0],
        [1.8, 0]
    ]  # Interesting initial positions
    
    # Draw Boundary
    theta = np.linspace(0, 2*np.pi, 100)
    x = 2*np.cos(theta)
    y= np.sin(theta)
    ax1.plot(x, y, color="k")
    for position in positions:
        ax1.scatter(position[0], position[1], marker='o', s=50, color="r", zorder=3)  # Plot starting position
        x, y, phase_x, phase_y = elliptical_geometry(position, 45, [2, 1], 1000, plot=False)
        ax1.plot(x, y)
        ax2.scatter(phase_x, phase_y, label=f"Start Position: ({round(position[0], 1)}, {round(position[1], 1)})")
    
    # Titles And Plot Tidying
    ax1.set_aspect("equal")
    ax1.set_title("Plot of Trajectories")
    ax1.set_xlabel("$x$")
    ax1.set_ylabel("$y$")
    ax2.set_xlim([0, 6.5])  # Makes space for legend
    ax2.legend()
    ax2.set_aspect("equal")
    ax2.set_title("Combined Phase Space Plot")
    ax2.set_xlabel("$s$")
    ax2.set_ylabel("$\cos{\\theta}$")
    fig.suptitle("Elliptical billiards demo with semi-major axis $a=2$, semi-minor axis $b=1$\n and ball hit at 45 degrees to the x axis", fontsize=16)
    fig.set_facecolor('lightgrey')
    plt.show()
    
def bunimovich_geometry(pos, init_angle, dims, reflections, plot=True):
    """Main Bunimovich Billiards Function
    
        - Draws bunimovich statium
        - Works out trajectories for specified number of collisions
        - Records points of collisions and plots
        - Records boundary perimeter from right-most point to collision point, 
          cosine of angle between velocity and tangent vector, and plots phase space
        
    Parameters
    ----------
        pos: 1D array
            starting position of billiard ball as an [x, y] array.
        init_angle: float
            angle in degrees at which billiard ball is hit
        reflections: int
            number of reflections to calculate (default=100)
        plot: bool
            flag for whether to display the various plots (default=True)
    """
    global ani  # Needed for animation (due to issues within Python)
    
    central_width, central_height = dims
    end_radius = central_height/2
    vel = [np.cos(np.radians(init_angle)), np.sin(np.radians(init_angle))]  # Initial velocity
    
    # Setting things up
    collisions_x = [pos[0]]  # This and below line needed to plot the start point
    collisions_y = [pos[1]]
    arc_length = []
    cos_angle = []
    max_t = central_width + central_height  # Maximum amount of time it would take for a collision to occur
    t = np.arange(0, 1.1*max_t, 1e-3)
    for i in range(reflections):
        # Work out future x and y values
        x_test = pos[0] + vel[0]*t
        y_test = pos[1] + vel[1]*t
        
        # Calculate collisions with the top and bottom
        tb_coll = np.where(y_test < -central_height/2)[0]  # See if anything is below the bottom
        if not np.any(tb_coll):  # If not bottom, try top
            tb_coll = np.where(y_test > central_height/2)[0]
        if not np.any(tb_coll):  # If not, no collision with top or bottom
            tb_coll = [len(x_test)]  # Set to index higher than any legitimate collision index
        tb_coll = tb_coll[0]  # First time out of boundary = first time colliding with boundary in this near-continuous case
        
        # Calculate collisions with the ends
        f_left = np.round(x_test+central_width/2 + np.sqrt(np.abs(end_radius**2 - y_test**2)), 2)[1:]  # Function of right-end semicircular boundary
        f_right = np.round(x_test-central_width/2 - np.sqrt(np.abs(end_radius**2 - y_test**2)), 2)[1:]  # Function of left-end semicircular boundary
        left_right_end = -1  # Used when calculating normal and tangent vectors
        end_coll = np.where(f_right>=0)[0]  # See if anything is beyond the right-end boundary
        if not np.any(end_coll):  # If not right, try left
            end_coll = np.where(f_left<=0)[0]
            left_right_end = 1  # Assume that if there's nothing hitting the right, then it must hit the left
        if not np.any(end_coll):  # If not, no collision with ends
            end_coll = [len(x_test)]
        end_coll = end_coll[0]
        
        # Find the point of collision with boundary
        coll_index = min(tb_coll, end_coll)  # Pick whatever we collided with first
        collision = [x_test[coll_index], y_test[coll_index]]
        if coll_index == tb_coll:  # If collided with top or bottom, reverse y velocity
            in_circle = False  # Used later on for phase space calculations
            vel[1]=-vel[1]
            tang_vec = [1, 0]
        else:  # Otherwise, calculate normal/tangent vectors and use those to change velocity
            in_circle = True
            diff_x = 2*(collision[0]+(central_width/2)*left_right_end)
            diff_y = 2*collision[1]
            norm_vec = [diff_x, diff_y]/np.sqrt(diff_x**2 + diff_y**2)  # Normal unit vector
            tang_vec = [-diff_y, diff_x]/np.sqrt(diff_x**2 + diff_y**2)  # Tangent unit vector
            vel = -1*np.dot(vel, norm_vec)*norm_vec + np.dot(vel, tang_vec)*tang_vec
        pos = collision  # Update ball's position
        collisions_x.append(pos[0])
        collisions_y.append(pos[1])
        
        cos = np.dot(vel, tang_vec)  # Get cosine of angle trajectory makes with tangent
        cos_angle.append(cos)  # y-axis of phase space plot

        # Arc Length Calculation
        box_perimeter = 2*central_width
        semicircle_perimeter = np.pi*central_height/2
        s = 0
        if in_circle:
            if pos[0] > 1:  # If in right circle
                angle = np.arctan(pos[1]/(pos[0]-central_width/2))
                if pos[1] <= 0:  # If below center of circle
                    angle += np.pi/2
                    s += box_perimeter + 3/2 * semicircle_perimeter
                s += end_radius * angle
            else:  # If in left circle
                s += box_perimeter/2 + semicircle_perimeter/2
                angle = np.arctan(pos[1]/(pos[0]+central_width/2)) - np.pi/2
                if round(angle, 3) <= 0:
                    angle += np.pi
                s += end_radius * angle
        else:
            if pos[1] > 0:  # If colliding with top
                s+= semicircle_perimeter/2 + central_width/2 - pos[0]
            else:  # Otherwise, colliding with bottom
                s+= semicircle_perimeter * 3/2 + central_width + pos[0] + central_width/2
        arc_length.append(s)  # x-axis of phase space plot
    arc_length = np.array(arc_length)
    cos_angle = np.array(cos_angle)
    if plot:
        fig, (ax1, ax2) = plt.subplots(2, 1)
        
        # DRAW THE STADIUM
        # Top and Bottom Lines
        top_bottom = np.linspace(-central_width/2, central_width/2, 100)
        top_line = np.ones(top_bottom.shape) * central_height/2
        bottom_line = -top_line
        ax1.plot(top_bottom, top_line, color='k')
        ax1.plot(top_bottom, bottom_line, color='k')
        
        # Ends
        theta = np.linspace(-np.pi/2, np.pi/2, 100)
        x_right = central_width/2 + end_radius * np.cos(theta)
        y_right = end_radius * np.sin(theta)
        ax1.plot(x_right, y_right, color="k")
        x_left = -central_width/2 + end_radius * np.cos(theta+np.pi)
        y_left = end_radius * np.sin(theta+np.pi)
        ax1.plot(x_left, y_left, color="k")
        
        # Animate plotting trajectories
        line, = ax1.plot(collisions_x, collisions_y)
        ani = animation.FuncAnimation(fig, update, len(collisions_x), interval=50*100/reflections, fargs=[collisions_x, collisions_y, line], blit=True, repeat=False)
    
        # Titles And Plot Tidying
        fig.set_facecolor('lightgrey')
        fig.suptitle(f"Mathematical Billiards in a Bunimovich Stadium table with central width $w={central_width}$, central height $h={central_height}$\n with the ball initially at ({collisions_x[0]}, {collisions_y[0]}) and hit at an angle of $\\theta = {init_angle}\degree$", fontsize=16)
        ax1.set_title(f"Trajectories in Real Space ({reflections} Collisions)")
        ax1.scatter(collisions_x[0], collisions_y[0], marker='o', s=50,color="r", zorder=3, label="Initial Position")  # Plot starting position
        ax1.set_xlabel("$x$ Position")
        ax1.set_ylabel("$y$ Position")
        ax2.set_title(f"Phase Space")
        ax2.scatter(arc_length, cos_angle)
        ax2.set_xlabel("$s$")
        ax2.set_ylabel(r"$\cos{\theta}$")
        ax1.legend()
        plt.show() 

def input_test(user_input, integer = False, positive = False):
    """User Input Testing Function
    
    Checks if user input is either a float or an integer or if its positive (depending on the prompt).
    
    Parameters
    ----------
        user_input: str
            the input to be tested
        integer: bool
            flag for whether the input needs to be an integer 
        positive: bool
            flag for whether the input needs ot be positive
    """
    if integer:
        try:
            user_input = int(user_input)
        except ValueError:
            print("NO! Enter a valid number!!!!!! 5 second sin bin.")
            sleep(5)
            main()
    else:
        try:
            user_input = float(user_input)
        except ValueError:
            print("NO! Enter a valid number!!!!!! 5 second sin bin.")
            sleep(5)
            main()
    if positive:
        if user_input <= 0:
            print("NO! Enter a valid number!!!!!! 5 second sin bin.")
            sleep(5)
            main()
    return user_input

def main():
    """Main Function
    
        - Provides a text-based menu system for the user to interact with
        - Handles unacceptable inputs to any of the prompts
    """
    print('''
          Welcome!!!!!

              1. Box Billiards
              2. Elliptical Billiards
              3. Bunimovich Billiards
              4. Interesting Elliptical Billiards Demo
              5. Exit
              ''')
    choice = input("What do you fancy???\n")
    choice = input_test(choice, integer=True)
    if choice < 1 or choice > 5:  # If user enters invalid number, throw up an error and ask again
        print("NO! Pick a proper number! 5 second sin bin.")
        sleep(5)
        main()
    if choice==5:
        exit()
    elif choice==1:
        width = input("How wide do you want the table?\n")
        width = input_test(width, positive=True)        
        height = input("How tall do you want the table?\n")
        height = input_test(height, positive=True)
        x = input("What's the starting x position?\n")
        x = input_test(x)
        if abs(x) > width/2:
            print("That's not on the table!!!! Remember the origin is the centre of the table.")
            sleep(3)
            main()
        y = input("What's the starting y position?\n")
        y = input_test(y)
        if abs(y) > height/2:
            print("That's not on the table!!!! Remember the origin is the centre of the table.")
            sleep(3)
            main() 
        angle = input("What angle do you fancy hitting the ball at (in degrees)?\n")
        angle = input_test(angle)
        reflections = input("How many collisions would you like to see?\n")
        reflections = input_test(reflections, integer=True, positive=True)
        print("Wait...")
        box_geometry([x, y], [np.cos(np.radians(angle)), np.sin(np.radians(angle))], [width, height], reflections)
        exit()
    elif choice==2:
        a = input("What's the semi-major axis?\n")
        a = input_test(a, positive = True)
        b = input("What's the semi-minor axis?\n")
        b = input_test(b, positive = True)
        if a < b:
            print("Can't have semi-major axis shorter than semi-minor axis!!!")
            sleep(2)
            main()
        x = input("What's the starting x position?\n")
        x = input_test(x)
        y= input("What's the starting y position?\n")
        y = input_test(y)
        if (x/a)**2 + (y/b)**2 > 1:
            print("That's not on the table!!!! Remember the origin is the centre of the table.")
            sleep(3)
            main()
        angle = input("What angle do you fancy hitting the ball at (in degrees)?\n")
        angle = input_test(angle)
        reflections = input("How many collisions would you like to see?\n")
        reflections = input_test(reflections, integer=True, positive=True)
        print("Wait...")
        elliptical_geometry([x, y], angle, [a, b], reflections)
        exit()
    elif choice==3:
        width = input("What central width do you want?\n")
        width = input_test(width, positive=True)
        height = input("What central height do you want?\n")
        height = input_test(height, positive=True)
        x = input("What's the starting x position?\n")
        x = input_test(x)
        y = input("What's the starting y position?\n")
        y = input_test(y)
        if x > width/2 and x-width/2 > np.sqrt((height/2)**2-y**2):
            print('Error!!! Not In Stadium!!!!')
            sleep(2)
            main()
        elif x < width/2 and x+width/2 < -np.sqrt((height/2)**2-y**2):
            print('Error!!! Not In Stadium!!!!')
            print('this one')
            sleep(2)
            main()
        elif abs(y) > height/2:
            print('Error!!!! Not In Stadium!!!')
            sleep(2)
            main()
        angle = input("What angle do you want to hit the ball at?\n")
        angle = input_test(angle)
        reflections = input("How many collisions would you like to see?\n")
        reflections = input_test(reflections, integer=True, positive=True)
        print("Wait...")
        bunimovich_geometry([x, y], angle, [width, height], reflections)
        exit()
    else:
        print("Wait...")
        elliptical_demo()
        exit()

main()
