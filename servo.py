from fpioa_manager import fm, board_info
from machine import Timer,PWM
import time

fm.register(board_info.JTAG_TCK,fm.fpioa.GPIO0)
tim1 = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
ch1 = PWM(tim1, freq=50, duty=5, pin=board_info.JTAG_TCK)
tim2 = Timer(Timer.TIMER1, Timer.CHANNEL0, mode=Timer.MODE_PWM)
ch2 = PWM(tim2, freq=50, duty=5, pin=board_info.JTAG_TDI)

while True:
    for x in range(180):
        duty = 5*(x/180)+5
        ch1.duty(duty)
        ch2.duty(duty)
        time.sleep(0.02)

    for x in range(180):
        duty = 5*(1-(x/180))+5
        ch1.duty(duty)
        ch2.duty(duty)
        time.sleep(0.02)
