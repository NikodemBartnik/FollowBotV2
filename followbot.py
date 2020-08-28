# Hello World Example
#
# Welcome to the MaixPy IDE!
# 1. Conenct board to computer
# 2. Select board at the top of MaixPy IDE: `tools->Select Board`
# 3. Click the connect buttion below to connect board
# 4. Click on the green run arrow button below to run the script!

import sensor, image, time, lcd
from fpioa_manager import fm, board_info
from machine import Timer,PWM
from Maix import GPIO

PWM_MOTOR = 35

#Setting up PWM to control servo motors
fm.register(board_info.JTAG_TCK,fm.fpioa.GPIO0)
tim1 = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
ch1 = PWM(tim1, freq=50, duty=5, pin=board_info.JTAG_TCK)
tim2 = Timer(Timer.TIMER1, Timer.CHANNEL0, mode=Timer.MODE_PWM)
ch2 = PWM(tim2, freq=50, duty=5, pin=board_info.JTAG_TDI)

fm.register(board_info.PIN10, fm.fpioa.GPIOHS1, force=True)
fm.register(board_info.PIN11, fm.fpioa.GPIOHS2, force=True)
fm.register(board_info.LED_B, fm.fpioa.GPIOHS3, force=True)
fm.register(board_info.LED_G, fm.fpioa.GPIOHS4, force=True)

#PWM for DC motors
tim3 = Timer(Timer.TIMER2, Timer.CHANNEL0, mode=Timer.MODE_PWM)
ENA = PWM(tim3, freq=50, duty=7, pin=board_info.PIN9)
tim4 = Timer(Timer.TIMER2, Timer.CHANNEL1, mode=Timer.MODE_PWM)
ENB = PWM(tim4, freq=50, duty=7, pin=board_info.LED_R)

IN1 = GPIO(GPIO.GPIOHS1, GPIO.OUT)
IN2 = GPIO(GPIO.GPIOHS2, GPIO.OUT)
IN3 = GPIO(GPIO.GPIOHS3, GPIO.OUT)
IN4 = GPIO(GPIO.GPIOHS4, GPIO.OUT)

IN1.value(0)
IN2.value(0)
IN3.value(0)
IN4.value(0)


def forward(MOTOR_POWER):
    ENA.duty(MOTOR_POWER)
    ENB.duty(MOTOR_POWER)
    IN1.value(1)
    IN2.value(0)
    IN3.value(1)
    IN4.value(0)


def back():
    ENA.duty(PWM_MOTOR)
    ENB.duty(PWM_MOTOR)
    IN1.value(0)
    IN2.value(1)
    IN3.value(0)
    IN4.value(1)


def left(MOTOR_POWER):
    ENA.duty(MOTOR_POWER)
    ENB.duty(MOTOR_POWER)
    IN1.value(0)
    IN2.value(1)
    IN3.value(1)
    IN4.value(0)


def right(MOTOR_POWER):
    ENA.duty(MOTOR_POWER)
    ENB.duty(MOTOR_POWER)
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



lcd.init(freq=15000000)
sensor.reset()
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)
sensor.run(1)
FRAME_C_W = 160
FRAME_C_H = 120
ACCEPTABLE_ERROR_IN_FRAMING = 30
pan_servo_duty = 7.5
tilt_servo_duty = 8
clock = time.clock()                # Create a clock object to track the FPS.

while(True):
    clock.tick()
    img = sensor.snapshot()
    img.replace(hmirror=True)
    blobs = img.find_blobs([(33, 73, 29, 75, -7, 44)], merge = True, margin = 10)
    biggest_blob = 0
    if blobs:
        biggest_blob = blobs[0]
        for b in blobs:
            if (b.w()*b.h()) > (biggest_blob.w() * biggest_blob.h()):
                biggest_blob = b

    if biggest_blob:
        img.draw_circle(biggest_blob.cx(), biggest_blob.cy(), 20)
        x = biggest_blob.cx()
        y = biggest_blob.cy()
        pixels_number = biggest_blob.pixels()
        strToPrint =  "X: %d Y: %d P: %d" % (x, y, pixels_number)
        img.draw_string(10, 10, strToPrint)

        if x > (FRAME_C_W + ACCEPTABLE_ERROR_IN_FRAMING):
            pan_servo_duty -= 0.3
        elif x < (FRAME_C_W - ACCEPTABLE_ERROR_IN_FRAMING):
            pan_servo_duty += 0.3

        if y > (FRAME_C_H + ACCEPTABLE_ERROR_IN_FRAMING):
            tilt_servo_duty -= 0.2
        elif y < (FRAME_C_H - ACCEPTABLE_ERROR_IN_FRAMING):
            tilt_servo_duty += 0.2



        if pixels_number < 4000:
            if pan_servo_duty > 8.5:
                left(PWM_MOTOR)
            elif pan_servo_duty < 6.5:
                right(PWM_MOTOR)
            else:
                forward(((1-pixels_number/4000)*30)+25)
        elif pixels_number > 8000:
            back()
        else:
            stop()


        if pan_servo_duty > 10:
            pan_servo_duty = 10
        elif pan_servo_duty < 5:
            pan_servo_duty = 5

        if tilt_servo_duty > 10:
            tilt_servo_duty = 10
        elif tilt_servo_duty < 5:
            tilt_servo_duty = 5
    else:
        left(40)
        pan_servo_duty = 7.5
        tilt_servo_duty = 8

    ch1.duty(pan_servo_duty)
    ch2.duty(tilt_servo_duty)
    lcd.display(img)
