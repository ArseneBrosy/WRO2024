#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time

ev3 = EV3Brick()
leftMotor = Motor(Port.C)
rightMotor = Motor(Port.B)

leftMotor.run_angle(200, -30, wait=False)
rightMotor.run_angle(200, -30)
rightMotor.run_angle(500, 360)
rightMotor.run(200)
leftMotor.run_angle(200, 1100)
rightMotor.hold()
