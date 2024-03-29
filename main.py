#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time

#region Constants
SPEED = 500;
SLOW_SPEED = 200;
VERY_SLOW_SPEED = 50;
WHITE_THRESHOLD = 70;
BLACK_THRESHOLD = 15;
LINE_AVERAGE = 35
KP = 2;
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
def runAngle(speed, degrees):
    leftMotor.run(speed if degrees > 0 else -speed)
    rightMotor.run_angle(speed, degrees)
    leftMotor.hold()

def runTime(speed, time):
    leftMotor.run(speed)
    rightMotor.run_time(speed, time)
    leftMotor.hold()

def alignementLine(speed):
    leftMotor.run(speed)
    rightMotor.run(speed)
    leftStopped = False
    rightStopped = False
    while not leftStopped or not rightStopped:
        if leftColorSensor.reflection() < BLACK_THRESHOLD and not leftStopped:
            leftMotor.hold()
            leftStopped = True
        if rightColorSensor.reflection() < BLACK_THRESHOLD and not rightStopped:
            rightMotor.hold()
            rightStopped = True

def followLine(speed, degree, sensor = 0):
    leftMotor.reset_angle(0)
    while leftMotor.angle() < degree:
        error = LINE_AVERAGE - (leftColorSensor.reflection() if sensor == 0 else rightColorSensor.refletion())
        correction = error * KP
        leftMotor.run(speed - correction)
        rightMotor.run(speed + correction)
    leftMotor.hold()
    rightMotor.hold()

def followLineUntilLine(speed, sensor = 0):
    lineSensor = rightColorSensor if sensor == 0 else leftColorSensor
    while lineSensor.reflection() > BLACK_THRESHOLD:
        error = LINE_AVERAGE - (leftColorSensor.reflection() if sensor == 0 else rightColorSensor.refletion())
        correction = error * KP
        leftMotor.run(speed - correction)
        rightMotor.run(speed + correction)
    leftMotor.hold()
    rightMotor.hold()

# Claw
def openClaw():
    clawMotor.run_time(1000, 500)

def closeClaw():
    clawMotor.run_time(-1000, 500)
#endregion

def programBase1():
    openClaw()

    # Take the blocks
    runAngle(VERY_SLOW_SPEED, -30)
    rightMotor.run_angle(SPEED, 360)
    runAngle(SLOW_SPEED, 1100)
    closeClaw()

    # Go to the red square
    runAngle(SPEED, -360)
    rightMotor.run_angle(SPEED, 360)
    runTime(-SLOW_SPEED, 2000)
    alignementLine(VERY_SLOW_SPEED)

    leftMotor.run_angle(SLOW_SPEED, 460)
    leftMotor.run(-SLOW_SPEED)
    rightMotor.run(-SLOW_SPEED)
    while leftColorSensor.reflection() > BLACK_THRESHOLD:
        pass
    runAngle(SLOW_SPEED, 400)
    leftMotor.run(-SLOW_SPEED)
    while leftColorSensor.reflection() > BLACK_THRESHOLD:
        pass
    followLine(SLOW_SPEED, 400)
    runAngle(SLOW_SPEED, 260)
    followLineUntilLine(SLOW_SPEED)
    
    leftMotor.run_angle(SLOW_SPEED, -480)
    rightMotor.run_angle(SLOW_SPEED, -480)
    runAngle(SLOW_SPEED, 50)

programBase1()
wait(2000)