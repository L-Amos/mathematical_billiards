# %matplotlib qt5
# -*- coding: utf-8 -*-
# pylint: disable=C0301, R1707, C0411, W0612, W0601, C0103, C0303
""" Encryption Using Mathematical Billiards

This program encrypts and decrypts data using a simulation of mathematical billiards on a Bunimovich-stadium table.

Author:
    Luke Amos
    University of Birmingham
    Student ID: 2297692

Created on Tue Oct 17 16:39:42 2023
"""
# Imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from time import sleep  # For menu options
from sys import exit

## For Encryption
from hashlib import sha256
from Crypto.Cipher import AES

# Stadium Dimensions
CENTRAL_WIDTH = 2+1e-15
CENTRAL_HEIGHT = 1
END_RADIUS = CENTRAL_HEIGHT/2

def bunimovich_geometry(angle):
    """Main Bunimovich Billiards Function
    
        - Draws bunimovich statium
        - Works out trajectories for 1000 collisions
        - Calculates boundary perimeter from right-most point to collision point and 
          cosine of angle between velocity and tangent vector
        - Returns a transformation of the last recorded boundary perimiter and cosine
        
    Parameters
    ----------
        angle: float
            angle in radians at which billiard ball is hit    
    Returns
    -------
        key: int
            transformation of the last recorded boundary perimiter and cosine, used as key in encryption  
    """
    
    pos=[0, 0]
    vel = [np.cos(angle), np.sin(angle)]  # Initial velocity
    
        # Setting things up
    collisions_x = [pos[0]]  # This and below line needed to plot the start point
    collisions_y = [pos[1]]
    arc_length = []
    cos_angle = []
    max_t = CENTRAL_WIDTH + CENTRAL_HEIGHT  # Maximum amount of time it would take for a collision to occur
    t = np.arange(0, 1.1*max_t, 1e-3)
    for i in range(1000):
        # Work out future x and y values
        x_test = pos[0] + vel[0]*t
        y_test = pos[1] + vel[1]*t    
        
        # Calculate collisions with the top and bottom
        tb_coll = np.where(y_test < -CENTRAL_HEIGHT/2)[0]  # See if anything is below the bottom
        if not np.any(tb_coll):  # If not bottom, try top
            tb_coll = np.where(y_test > CENTRAL_HEIGHT/2)[0]
        if not np.any(tb_coll):  # If not, no collision with top or bottom
            tb_coll = [len(x_test)]  # Set to index higher than any legitimate collision index
        tb_coll = tb_coll[0]  # First time out of boundary = first time colliding with boundary in this near-continuous case
        
        # Calculate collisions with the ends
        f_left = np.round(x_test+CENTRAL_WIDTH/2 + np.sqrt(np.abs(END_RADIUS**2 - y_test**2)), 2)[1:]  # Function of right-end semicircular boundary
        f_right = np.round(x_test-CENTRAL_WIDTH/2 - np.sqrt(np.abs(END_RADIUS**2 - y_test**2)), 2)[1:]  # Function of left-end semicircular boundary
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
            diff_x = 2*(collision[0]+(CENTRAL_WIDTH/2)*left_right_end)
            diff_y = 2*collision[1]
            norm_vec = [diff_x, diff_y]/np.sqrt(diff_x**2 + diff_y**2)  # Normal unit vector
            tang_vec = [-diff_y, diff_x]/np.sqrt(diff_x**2 + diff_y**2)  # Tangent unit vector
            vel = -1*np.dot(vel, norm_vec)*norm_vec + np.dot(vel, tang_vec)*tang_vec
        pos = collision
        collisions_x.append(pos[0])
        collisions_y.append(pos[1])
        
        # Arc Length Calculation
        box_perimeter = 2*CENTRAL_WIDTH
        semicircle_perimeter = np.pi*CENTRAL_HEIGHT/2
        s = 0
        if in_circle:
            if pos[0] > 1:  # If in right circle
                angle = np.arctan(pos[1]/(pos[0]-CENTRAL_WIDTH/2))
                if pos[1] <= 0:  # If below center of circle
                    angle += np.pi/2
                    s += box_perimeter + 3/2 * semicircle_perimeter
                s += END_RADIUS * angle
            else:  # If in left circle
                s += box_perimeter/2 + semicircle_perimeter/2
                angle = np.arctan(pos[1]/(pos[0]+CENTRAL_WIDTH/2)) - np.pi/2
                if round(angle, 3) <= 0:
                    angle += np.pi
                s += END_RADIUS * angle
        else:
            if pos[1] > 0:  # If colliding with top
                s+= semicircle_perimeter/2 + CENTRAL_WIDTH/2 - pos[0]
            else: 
                s+= semicircle_perimeter * 3/2 + CENTRAL_WIDTH + pos[0] + CENTRAL_WIDTH/2
        arc_length.append(s)
    arc_length = np.array(arc_length)
    key = arc_length[-1]/(box_perimeter + 2*semicircle_perimeter)  # Normalised arc length
    return key  

def encrypt(path, plaintext):
    """Encryption Function
    
        - Takes an angle and a file path and plaintext
        - Uses the angle with Bunimovich billiards to create a key
        - Uses the hashed key to encrypt the plaintext (using AES) and writes the angle and iv used
          to the file at the specified file path
    
    Parameters
    ----------
        path: str 
            file path to save output to.
        plaintext: str 
            string to be encrypted.
    """
    angle = input("What angle (in degrees) do you wanna hit your ball at?\n")
    try:  # Test if user input is valid
        angle = float(angle)
    except ValueError:
        print("NO! Enter a valid angle!!!!!! 5 second sinbin.")
        sleep(5)
        main()
    print("Encrypting...")
    angle = np.radians(angle)
    unhashed_key = str(bunimovich_geometry(angle))
    key = sha256(unhashed_key.encode('utf-8')).digest()
    aes = AES.new(key, AES.MODE_CFB)
    ciphertext = aes.encrypt(plaintext.encode('utf8'))
    with open(path, "w", encoding="utf-8") as f:
        f.write(str(angle)+'\n')
        f.write(str(aes.iv.hex())+'\n')  # Write in hex form to make it nicer to look at
        f.write(str(ciphertext.hex())+'\n')
    
def file_encrypt():
    """File Encryption Function
    
        - Ingests a file at a specified path
        - Overwrites file with encrypted contents
    """
    file_path = input("Where's the file?\n")
    try:
        with open(file_path, 'r', encoding="utf-8") as f:
            plaintext = f.read()
    except FileNotFoundError:
        print('File not found!!!!!')
        sleep(2)
        main()
    encrypt(file_path, plaintext)
    print("Done!")
    sleep(1)
    main()

def decrypt():
    """Decryption Function
    
        - Ingests an encrypted file at a specified path
        - Retrieves an iv and angle from the file
        - Uses the angle and Bunimovich billiards to create a key
        - Hashed key and iv used to decrypt the file (using AES)
        - Contents of file replaced with decrypted contents
        - If decryption fails, file's encrypted contents fully restored and error message thrown up
    """
    file_path = input("Where's the encrypted file bud?\n")
    try:
        with open(file_path, 'r', encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("File not found!!!!")
        sleep(2)
        main()
    print("Decrypting...")
    angle = float(lines[0])
    iv = bytes.fromhex(lines[1])  # Initialisation vector for AES
    ciphertext = bytes.fromhex(lines[2])
    unhashed_key = str(bunimovich_geometry(angle))
    key = sha256(unhashed_key.encode('utf-8')).digest()
    aes = AES.new(key, AES.MODE_CFB, iv=iv)
    plaintext = aes.decrypt(ciphertext)
    with open(file_path, "w", encoding="utf-8") as f:
        try:  # Test if decryption worked
            f.write(plaintext.decode('utf-8'))
            print('Done!')
            sleep(1)
        except UnicodeDecodeError:
            for line in lines:
                f.write(line)
            print("INTRUDER!!!!! INTRUDER!!!!")
            sleep(3)
    main()

def main():
    global CENTRAL_WIDTH, CENTRAL_HEIGHT, END_RADIUS
    """Main Function
    
        - Provides a text-based menu system for the user to interact with
        - Handles unacceptable inputs to any of the prompts
    """
    print('''
          Welcome!!!!!

              1. Encrypt String
              2. Encrypt File
              3. Decrypt
              4. Key Randomness Visualisation
              5. Exit
              ''')
    choice = input("What do you fancy???\n")
    try:
        choice = int(choice)
    except ValueError:  # If user doesn't put in a number, throw up an error and ask again
        print("NO! Put in a number! 5 second sinbin.")
        sleep(5)
        main()
    if choice < 1 or choice > 5:  # If user enters invalid number, throw up an error and ask again
        print("NO! Pick a proper number! 5 second sinbin.")
        sleep(5)
        main()
    # Exit
    if choice == 5:
        exit()
    # Encryption
    elif choice==1:
        file_path = input("Where do you want your encrypted file?\n")
        plaintext = input("What do you wanna encrypt?\n")
        encrypt(file_path, plaintext)
        print("Done!")
        sleep(1)
        main()
    # Decryption
    elif choice==2:
        file_encrypt()
    elif choice==3:
        decrypt()
    else:
        keys = []
        dims = np.linspace(0, 10, 500)
        angles = np.linspace(0, 2*np.pi, 500)
        for num in range(1000):
            # Simulate with random stadium dimensions to get 1000 random keys
            CENTRAL_WIDTH = np.random.choice(dims)
            CENTRAL_HEIGHT = np.random.choice(dims)
            END_RADIUS = CENTRAL_HEIGHT/2
            angle = np.random.choice(angles)
            keys.append(bunimovich_geometry(angle))
        fig, ax = plt.subplots()
        ax.hist(keys, bins=20)
        fig.set_facecolor('lightgrey')
        ax.set_xlabel("Value of unhashed key, $s$")
        ax.set_ylabel("Frequency")
        ax.set_title("Histogram of 1000 Random Unhashed Keys")
main()
