from __future__ import print_function

import time
from sr.robot import *

a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""

R = Robot()
""" instance of the class Robot"""

placed_token = []

seq = 0

def drive(speed, seconds):
    """
    Function for setting a linear velocity

    Args: speed (int): the speed of the wheels
          seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity

    Args: speed (int): the speed of the wheels
          seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_first_token():
    """
    Function to find the closest token

    Returns:
        dist (float): distance of the closest token (-1 if no token is detected)
        rot_y (float): angle between the robot and the  token (-1 if no token is detected)
    """
    dist = 100
    for token in R.see():
        if token.dist < dist:
            dist = token.dist
            rot_y = token.rot_y
            code = token.info.code
    if dist == 100:
        return -1, -1, -1
    else:
        return dist, rot_y, code

def find_token():
    """
    Function to find the closest token

    Returns:
        dist (float): distance of the closest token (-1 if no token is detected)
        rot_y (float): angle between the robot and the  token (-1 if no token is detected)
    """
    dist = 100
    for token in R.see():
        if token.dist < dist and token.info.code not in placed_token:
            dist = token.dist
            rot_y = token.rot_y
            code = token.info.code
    if dist == 100:
        return -1, -1, -1
    else:
        return dist, rot_y, code
    
def find_first_place(placed_token):
    """
    Function to find the closest token
    """
    dist = 100
    for token in R.see():
        if token.dist < dist and token.info.code == placed_token[0]:
            dist = token.dist
            rot_y = token.rot_y
    if dist == 100:
        return -1, -1
    else:
        return dist, rot_y

while 1:
    if seq == 0:
        token_dist, token_rot_y, token_code = find_first_token()
        if token_dist == -1:
            print('No token found')
            turn(5, 1)
        elif token_rot_y < -a_th:
            turn(-5, 0.25)
        elif token_rot_y > a_th:
            turn(5, 0.25)
        elif -a_th <= token_rot_y <= a_th:
            token_dist, token_rot_y, token_code = find_first_token()
            drive(10, 0.5)
            if token_dist < d_th:
                if R.grab():
                    turn(-10, 2)
                    drive(10, 3)
                    R.release()
                    drive(-10, 3)
                    placed_token.append(token_code)
                    print('Added token: ', token_code)
                    turn(-5, 3)
                    seq += 1
                    status = 'Finding token'
                    print(status)
                else:
                    print('Failed to grab')

    elif status == 'Finding token' and 0 < seq < 6:
        token_dist, token_rot_y, token_code = find_token()
        if token_dist == -1:
            print('No token found')
            turn(5, 1)
        elif token_rot_y < -a_th:
            turn(-5, 0.25)
        elif token_rot_y > a_th:
            turn(5, 0.25)
        elif -a_th <= token_rot_y <= a_th:
            token_dist, token_rot_y, token_code = find_token()
            drive(10, 0.5)
            if token_dist < d_th:
                if R.grab():
                    status = 'Finding place'
                    print(status)
                else:
                    print('Failed to grab')
    elif status == 'Finding place' and 0 < seq < 6:
        ref_dist, ref_rot = find_first_place(placed_token)
        if ref_dist == -1:
            print('No place found')
            turn(5, 1)
        elif ref_rot < -a_th:
            turn(-5, 0.25)
        elif ref_rot > a_th:
            turn(5, 0.25)
        elif -a_th <= ref_rot <= a_th:
            ref_dist, ref_rot = find_first_place(placed_token)
            drive(10, 0.5)
            if ref_dist < d_th+0.25:
                R.release()
                placed_token.append(token_code)
                print('Added token: ', token_code, seq)
                seq += 1
                drive(-10, 1.5)
                status = 'Finding token'
    elif seq > 5:
        print('Job completed!')
        exit()
