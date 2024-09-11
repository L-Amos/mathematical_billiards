from time import sleep
import sys
import numpy as np

def input_test(question, integer=True, positive=False):
    while True:
        user_input = input(question)
        if user_input.lower() == "q":
            sys.exit()  # Quit
        try:
            if integer:
                user_input = int(user_input)
            else:
                user_input = float(user_input)
        except ValueError:
            print("Error: input wrong type.")
            sleep(1)
        else:
            if positive and float(user_input) < 0:
                print("Error: must be positive.")
                sleep(1)
            else:
                break
    return user_input

def update(num, collisions_x, collisions_y, line):
    """Plot Update Function
    
    Animates plotting of trajectories.
    
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