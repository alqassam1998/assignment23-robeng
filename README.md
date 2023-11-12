# Robot Simulator

This repository contains code files that are necessary to run the robot simulator program for the first assignment of Research Track 1. 

## How to run the code

 1. Check the dependencies are properly installed from [this repository](https://github.com/CarmineD8/python_simulator/tree/assignment23_python3).
 2. Clone the repository `git clone https://github.com/alqassam1998/assignment23-robeng.git`
 3. Run `python3 run.py assignment.py`

## How the code works

The following pseudocode explains how the code works.
```
set sequence = 0
if sequence = 0:
	if token distance > 100:
		turn the robot
	if token distance <= 100:
		align the robot to the token
		drive forward the robot
		grab the token
		move the token closer to the center
		add token code to the picked token list
		drive backward the robot
		add sequence +1
if 0 < sequence < 6:
	if token not in the picked token list distance > 100:
		turn the robot
	if token distance <= 100:
		align the robot to the token
		drive forward the robot
		grab the token
		move the token closer to the center
		add token code to the picked token list
		drive backward the robot
		add sequence +1
else:
	end the job
```
## Possible Improvements
The code cannot detect the first token as the reference without moving it closer to the center.
