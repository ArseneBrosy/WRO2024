#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time

#region Constants
SPEED = 700;
SLOW_SPEED = 400;
VERY_SLOW_SPEED = 200;
WHITE_THRESHOLD = 70;
BLACK_THRESHOLD = 15;
LINE_AVERAGE = 35
KP = 2;
HEIGHTS = [0, 480, 740, 1020]
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
    '''
    leftMotor.run(speed if degrees > 0 else -speed)
    rightMotor.run_angle(speed, degrees)
    leftMotor.hold()
    '''
    leftMotor.run_angle(speed, degrees, wait = False)
    rightMotor.run_angle(speed, degrees)
    leftMotor.hold()
    rightMotor.hold()

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

def followLine(speed, degree, sensor = 0, kp = KP):
    leftMotor.reset_angle(0)
    while leftMotor.angle() < degree:
        error = LINE_AVERAGE - (leftColorSensor.reflection() if sensor == 0 else rightColorSensor.reflection())
        correction = error * kp
        leftMotor.run(speed - correction)
        rightMotor.run(speed + correction)
    leftMotor.hold()
    rightMotor.hold()

def followLineUntilLine(speed, sensor = 0, kp = KP):
    lineSensor = rightColorSensor if sensor == 0 else leftColorSensor
    while lineSensor.reflection() > BLACK_THRESHOLD:
        error = LINE_AVERAGE - (leftColorSensor.reflection() if sensor == 0 else rightColorSensor.reflection())
        correction = error * kp
        leftMotor.run(speed - correction)
        rightMotor.run(speed + correction)
    leftMotor.hold()
    rightMotor.hold()

def turn(speed, degrees):
    leftMotor.run(speed if degrees > 0 else -speed)
    rightMotor.run_angle(speed, -degrees)
    leftMotor.hold()

# Claw
def openClaw():
    clawMotor.run_time(1000, 500)

def closeClaw():
    clawMotor.run_time(-1000, 750)

def raiseClaw(height):
    liftMotor.reset_angle(0)
    liftMotor.run(10000)
    timer = StopWatch()
    while liftMotor.angle() < height and timer.time() < 4000:
        pass
    liftMotor.hold()

def lowerClaw(wait = False):
    liftMotor.run_time(-1000, 800 if wait else 2000, wait = wait)

def placePiece(height, distance = 0, correctionDegree = 0):
    runAngle(VERY_SLOW_SPEED, max(100 - distance, 0))
    runAngle(VERY_SLOW_SPEED, -max(100 - distance, 0))
    if height > 0:
        raiseClaw(HEIGHTS[height])
    if distance > 0:
        runAngle(VERY_SLOW_SPEED, -distance)
    turn(SLOW_SPEED, correctionDegree)
    openClaw()
    liftMotor.run_time(1000, 700)
    if height == 3:
        runAngle(VERY_SLOW_SPEED, 200)
        lowerClaw()
    else:
        if height > 0:
            runAngle(VERY_SLOW_SPEED, 130)
            lowerClaw() 
        runAngle(VERY_SLOW_SPEED, 65 + max(distance, 80) - (130 if height > 0 else 0) + (30 if height > 0 else 0))
        if height == 0:
            lowerClaw(True)
            runAngle(VERY_SLOW_SPEED, 30)

def buildTower():
    placePiece(0)
    closeClaw()
    placePiece(1, 175)
    closeClaw()
    placePiece(2, 260)
    closeClaw()
    placePiece(3, 350, False)

#endregion

#region Program
def waitForButton():
    ev3.screen.draw_text(0, 0, "Prêt à partir")
    ev3.screen.draw_text(0, 30, "Vérifier prenneurs")
    ev3.screen.draw_text(0, 60, "Vérifier roues pince")
    ev3.screen.draw_text(0, 90, "Vérifier câble pince")
    while Button.CENTER not in ev3.buttons.pressed():
        pass

def programBase1():
    openClaw()

    # Take the blocks
    runAngle(SLOW_SPEED, -40)
    rightMotor.run_angle(SPEED, 340)
    runAngle(SPEED, 700)

    # Go to the 2 other pieces
    runAngle(SPEED, -560)
    rightMotor.run_angle(SPEED, 220)
    leftMotor.run(SLOW_SPEED)
    rightMotor.run(SLOW_SPEED)
    while leftColorSensor.reflection() > BLACK_THRESHOLD:
        pass
    wait(200)
    while leftColorSensor.reflection() > BLACK_THRESHOLD:
        pass
    runAngle(SLOW_SPEED, 130)
    leftMotor.run(-SLOW_SPEED)
    rightMotor.run(SLOW_SPEED)
    while leftColorSensor.reflection() > BLACK_THRESHOLD:
        pass
    wait(50)

    # follow line
    followLine(SLOW_SPEED, 260)
    runAngle(SLOW_SPEED, 260)
    followLineUntilLine(SLOW_SPEED)

    # align to line
    rightMotor.hold()
    leftMotor.run_angle(SLOW_SPEED, 100)
    leftMotor.run(SLOW_SPEED)
    while leftColorSensor.reflection() > BLACK_THRESHOLD:
        pass
    leftMotor.hold()
    rightMotor.run_angle(SLOW_SPEED, 100)

    # follow line
    followLine(SLOW_SPEED, 200)

    # align to pieces
    runAngle(SLOW_SPEED, 200)
    rightMotor.run_angle(SPEED, 420)
    runAngle(SLOW_SPEED, 200)
    rightMotor.run_angle(SPEED, 400)

    # take the last 2 red pieces
    runAngle(SPEED, 650)
    closeClaw()

    # Go to the red square
    runAngle(SPEED, -560)
    rightMotor.run_angle(SPEED, 190)
    leftMotor.run(SLOW_SPEED)
    rightMotor.run(SLOW_SPEED)
    while leftColorSensor.reflection() > BLACK_THRESHOLD:
        pass
    wait(500)
    while leftColorSensor.reflection() > BLACK_THRESHOLD:
        pass
    runAngle(SLOW_SPEED, 200)
    leftMotor.run(-SLOW_SPEED)
    rightMotor.run(SLOW_SPEED)
    while leftColorSensor.reflection() > BLACK_THRESHOLD:
        pass
    wait(50)
    leftMotor.hold()
    rightMotor.hold()

    # follow line
    followLine(SLOW_SPEED, 175)
    runAngle(SLOW_SPEED, 100)

    # align to square
    rightMotor.run_angle(SPEED, 440)

    # push the debrit
    runAngle(SLOW_SPEED, -550)
    runAngle(SLOW_SPEED, 320)

    # build the tower
    buildTower()

    # go to the 4 pieces of the second tower
    leftMotor.run_angle(-SLOW_SPEED, 230, wait=False)
    rightMotor.run_angle(SLOW_SPEED, 230)
    alignementLine(-SLOW_SPEED)
    rightMotor.run_angle(-SLOW_SPEED, 600)

    # take the block
    runAngle(SPEED, 1150)
    closeClaw()

    # go to the yellow square
    runAngle(SLOW_SPEED, -580)
    rightMotor.run_angle(-SLOW_SPEED, 420)
    alignementLine(-SLOW_SPEED)
    leftMotor.run_angle(-SLOW_SPEED, 240, wait = False)
    rightMotor.run_angle(-SLOW_SPEED, 240)

    # build the tower
    buildTower()

def programBase2():
    openClaw()

    # Take the blocks
    runAngle(SLOW_SPEED, -40)
    rightMotor.run_angle(SPEED, 370)
    runAngle(SPEED, 700)

    # Go to the 2 red pieces
    rightMotor.run_angle(SLOW_SPEED, -150)
    runAngle(SPEED, -600)
    rightMotor.run_angle(SPEED, 230)
    leftMotor.run(SLOW_SPEED)
    rightMotor.run(SLOW_SPEED)
    while leftColorSensor.reflection() > BLACK_THRESHOLD:
        pass
    wait(500)
    while leftColorSensor.reflection() > BLACK_THRESHOLD:
        pass
    runAngle(SLOW_SPEED, 130)
    leftMotor.run(-VERY_SLOW_SPEED)
    rightMotor.run(VERY_SLOW_SPEED)
    while leftColorSensor.reflection() > BLACK_THRESHOLD:
        pass
    wait(50)

    # follow line
    followLine(SLOW_SPEED, 260)
    rightMotor.run_angle(SLOW_SPEED, 30)
    runAngle(SLOW_SPEED, 260)
    followLineUntilLine(SLOW_SPEED)

    # align to line
    rightMotor.hold()
    leftMotor.run_angle(SLOW_SPEED, 100)
    rightMotor.run_angle(SLOW_SPEED, -100)
    leftMotor.run(SLOW_SPEED)
    while leftColorSensor.reflection() > BLACK_THRESHOLD:
        pass
    leftMotor.hold()

    # align to pieces
    runAngle(SLOW_SPEED, 300)
    rightMotor.run_angle(SPEED, 420)
    runAngle(SLOW_SPEED, 250)
    rightMotor.run_angle(SPEED, 400)

    # take the last 2 red pieces
    runAngle(SPEED, 800)
    closeClaw()

    # Go to the red square
    rightMotor.run_angle(SLOW_SPEED, -150)
    runAngle(SPEED, -600)
    rightMotor.run_angle(SPEED, 250)
    leftMotor.run(SLOW_SPEED)
    rightMotor.run(SLOW_SPEED)
    while leftColorSensor.reflection() > BLACK_THRESHOLD:
        pass
    wait(250)
    runAngle(SLOW_SPEED, 200)
    leftMotor.run(-SLOW_SPEED)
    rightMotor.run(SLOW_SPEED)
    while leftColorSensor.reflection() > BLACK_THRESHOLD:
        pass
    wait(50)
    leftMotor.hold()
    rightMotor.hold()

    # follow line
    leftMotor.run(-SLOW_SPEED)
    rightMotor.run(-SLOW_SPEED)
    while rightColorSensor.reflection() > BLACK_THRESHOLD:
        pass
    runAngle(SLOW_SPEED, 50)
    followLine(SLOW_SPEED, 450)
    runAngle(SLOW_SPEED, 110)

    # align to square
    leftMotor.run_angle(SPEED, 440)

    # push the debrit
    runAngle(SLOW_SPEED, -780)
    runAngle(SLOW_SPEED, 340)

    # build the tower
    buildTower()

    # push the second debrit
    runAngle(SPEED, 2000)

    # push the third debrit
    leftMotor.run_angle(SLOW_SPEED, 230, wait=False)
    rightMotor.run_angle(-SLOW_SPEED, 230)

    runAngle(SPEED, -500)

    '''
    # go to the 4 pieces of the second tower
    leftMotor.run_angle(SLOW_SPEED, 300, wait=False)
    rightMotor.run_angle(-SLOW_SPEED, 300)
    runAngle(SLOW_SPEED, -500)
    alignementLine(-SLOW_SPEED)
    rightMotor.run_angle(-SLOW_SPEED, 600)

    # take the block
    runAngle(SPEED, 1150)
    closeClaw()

    # go to the yellow square
    runAngle(SLOW_SPEED, -580)
    rightMotor.run_angle(-SLOW_SPEED, 420)
    alignementLine(-SLOW_SPEED)
    leftMotor.run_angle(-SLOW_SPEED, 240, wait = False)
    rightMotor.run_angle(-SLOW_SPEED, 240)

    # build the tower
    buildTower()
    '''

waitForButton()
programBase2()
#endregion