#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time

ev3 = EV3Brick()

# Motors
leftMotor = Motor(Port.C)
rightMotor = Motor(Port.B)
claw = Motor(Port.D)
lift = Motor(Port.A)

#region Functions
# Wheels
def run_degree(power, degrees):
    leftMotor.run(power)
    rightMotor.run_angle(power, degrees)
    leftMotor.hold()

# Claw
def openClaw():
    claw.run_time(1000, 500)

def closeClaw():
    claw.run_time(-1000, 500)
#endregion

#region Program
# Take the blocks
run_degree(200, -30)

rightMotor.run_angle(500, 360)

run_degree(200, 1100)

closeClaw()
#endregion
