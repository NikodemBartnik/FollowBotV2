# Untitled - By: Nikodem - śr. sie 26 2020

import sensor, image, time, lcd
from fpioa_manager import fm, board_info
from machine import Timer,PWM
from Maix import GPIO
import utime


def forward():
    ENA.duty(50)
    ENB.duty(50)
    IN1.value(1)
    IN2.value(0)
    IN3.value(1)
    IN4.value(0)


def back():
    ENA.duty(50)
    ENB.duty(50)
    IN1.value(0)
    IN2.value(1)
    IN3.value(0)
    IN4.value(1)


def right():
    ENA.duty(50)
    ENB.duty(50)
    IN1.value(0)
    IN2.value(1)
    IN3.value(1)
    IN4.value(0)


def left():
    ENA.duty(50)
    ENB.duty(50)
    IN1.value(1)
    IN2.value(0)
    IN3.value(0)
    IN4.value(1)


def stop():
    ENA.duty(0)
    ENB.duty(0)
    IN1.value(0)
    IN2.value(0)
    IN3.value(0)
    IN4.value(0)


fm.register(board_info.PIN10, fm.fpioa.GPIOHS1, force=True)
fm.register(board_info.PIN11, fm.fpioa.GPIOHS2, force=True)
fm.register(board_info.LED_B, fm.fpioa.GPIOHS3, force=True)
fm.register(board_info.LED_G, fm.fpioa.GPIOHS4, force=True)

tim3 = Timer(Timer.TIMER2, Timer.CHANNEL0, mode=Timer.MODE_PWM)
ENA = PWM(tim3, freq=50, duty=60, pin=board_info.PIN9)
tim4 = Timer(Timer.TIMER2, Timer.CHANNEL1, mode=Timer.MODE_PWM)
ENB = PWM(tim4, freq=50, duty=60, pin=board_info.LED_R)

IN1 = GPIO(GPIO.GPIOHS1, GPIO.OUT)
IN2 = GPIO(GPIO.GPIOHS2, GPIO.OUT)
IN3 = GPIO(GPIO.GPIOHS3, GPIO.OUT)
IN4 = GPIO(GPIO.GPIOHS4, GPIO.OUT)



IN1.value(0)
IN2.value(0)
IN3.value(0)
IN4.value(0)

while True:
    forward()
    utime.sleep_ms(5000)
    back()
    utime.sleep_ms(5000)
    left()
    utime.sleep_ms(5000)
    right()
    utime.sleep_ms(5000)
    stop()
    utime.sleep_ms(5000)
