from time import sleep
import sys
import numpy as np

def input_test(question, integer=True, positive=False):
    """Asks user for input and then tests inputs are of the correct type and form.

    Parameters
    ----------
    question : str 
        Question to ask user to receive input.
    integer : bool, optional
        Flag for whether input needs to be an integer, by default True.
    positive : bool, optional
        Flag for whether input needs to be positive, by default False.

    Returns
    -------
    any
        Input of the correct type and form.
    """
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

def update(num, collisions_x, collisions_y, line, start_pos):
    """Animates plotting of trajectories.
    
    Parameters
    ----------
        num: int
            Serves as an incrementer.
        collisions_x: 1D array
            x coordinates of collision points.
        collisions_y: 1D array
            y coordinates of collision points.
        line: matplotlib object
            Line of the matplotlib plot.
        start_pos: matplotlib object
            Scatter point representing the starting position of the ball.
    
    Returns
    -------
        line: matplotlib object
            Updated line for matplotlib plot.
        start_pos: matplotlib object
            Scatter point representing the starting position of the ball.
    """
    line.set_data(collisions_x[:num+1], collisions_y[:num+1])
    return line, start_pos

def arc_length(angle, a, b):  
    """Integrated to calculate arc length of the ellipse from right-most point to point of collision.
    
    Parameters
    ----------
        angle: float
            Elliptical angle in radians.
        a: float
            Semi-major axis of the ellipse.
        b: float
           Semi-minor axis of the ellipse.
    
    Returns
    -------
        f: float
            Integrand of ellpise arc length calculation.
    """
    f = np.sqrt((a*np.cos(angle))**2+(b*np.sin(angle))**2)
    return f