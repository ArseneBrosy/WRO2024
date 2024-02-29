#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time

#region Constants
FAST_SPEED = 750;
SPEED = 500;
SLOW_SPEED = 200;
VERY_SLOW_SPEED = 50;
WHITE_THRESHOLD = 15;
BLACK_THRESHOLD = 70;
#endregion

ev3 = EV3Brick()

# Motors
leftMotor = Motor(Port.C)
rightMotor = Motor(Port.B)
clawMotor = Motor(Port.D)
liftMotor = Motor(Port.A)

# Sensors
leftColorSensor = ColorSensor(Port.S3)
rightColorSensor = ColorSensor(Port.S2)

#region Functions
# Wheels
def run_degree(speed, degrees):
    leftMotor.run(speed if degrees > 0 else -speed)
    rightMotor.run_angle(speed, degrees)
    leftMotor.hold()

def run_time(speed, time):
    leftMotor.run(speed)
    rightMotor.run_time(speed, time)
    leftMotor.hold()

def alignementLine(speed):
    leftMotor.run(speed)
    rightMotor.run(speed)
    leftStopped = False
    rightStopped = False
    while not leftStopped or not rightStopped:
        if leftColorSensor.reflection() < WHITE_THRESHOLD and not leftStopped:
            leftMotor.hold()
            leftStopped = True
        if rightColorSensor.reflection() < WHITE_THRESHOLD and not rightStopped:
            rightMotor.hold()
            rightStopped = True

# Claw
def openClaw():
    clawMotor.run_time(1000, 500)

def closeClaw():
    clawMotor.run_time(-1000, 500)
#endregion

#region Program
openClaw()

# Take the blocks
run_degree(VERY_SLOW_SPEED, -30)
rightMotor.run_angle(SPEED, 360)
run_degree(SLOW_SPEED, 1100)
closeClaw()

# Go to the red square
run_degree(SPEED, -360)
ev3.speaker.beep()
rightMotor.run_angle(SPEED, 360)
run_time(-SLOW_SPEED, 2000)
alignementLine(VERY_SLOW_SPEED)
leftMotor.run_angle(VERY_SLOW_SPEED, 100)                       
leftMotor.run(VERY_SLOW_SPEED)
while leftColorSensor.reflection() > WHITE_THRESHOLD:
    pass
leftMotor.hold()
#endregion
