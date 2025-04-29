"""
Example micropython program to run as a clock

Set the time with `mpremote connect port:/dev/ttyACM0 rtc --set`
Run with `mpremote connect port:/dev/ttyACM1 run example.py`

"""

import time
import machine

led = machine.Pin("LED", machine.Pin.OUT)
rtc = machine.RTC()

digits = [
    [
        machine.Pin(17, machine.Pin.OUT),  # IO0_A
        machine.Pin(18, machine.Pin.OUT),  # IO0_B
        machine.Pin(19, machine.Pin.OUT),  # IO0_C
        machine.Pin(16, machine.Pin.OUT),  # IO0_D
    ],
    [
        machine.Pin(2, machine.Pin.OUT),  # IO1_A
        machine.Pin(5, machine.Pin.OUT),  # IO1_B
        machine.Pin(7, machine.Pin.OUT),  # IO1_C
        machine.Pin(0, machine.Pin.OUT),  # IO1_D
    ],
    [
        machine.Pin(3, machine.Pin.OUT),  # IO2_A
        machine.Pin(4, machine.Pin.OUT),  # IO2_B
        machine.Pin(6, machine.Pin.OUT),  # IO2_C
        machine.Pin(1, machine.Pin.OUT),  # IO2_D
    ],
    [
        machine.Pin(15, machine.Pin.OUT),  # IO3_A
        machine.Pin(11, machine.Pin.OUT),  # IO3_B
        machine.Pin(10, machine.Pin.OUT),  # IO3_C
        machine.Pin(13, machine.Pin.OUT),  # IO3_D
    ],
    [
        machine.Pin(22, machine.Pin.OUT),  # IO4_A
        machine.Pin(8, machine.Pin.OUT),  # IO4_B
        machine.Pin(26, machine.Pin.OUT),  # IO4_C
        machine.Pin(9, machine.Pin.OUT),  # IO4_D
    ],
    [
        machine.Pin(21, machine.Pin.OUT),  # IO5_A
        machine.Pin(12, machine.Pin.OUT),  # IO5_B
        machine.Pin(14, machine.Pin.OUT),  # IO5_C
        machine.Pin(20, machine.Pin.OUT),  # IO5_D
    ],
]

def initialize_pins():
    for digit in digits:
        for bit in digit:
            bit.on()

    # dir_pin = machine.Pin(28, machine.Pin.OUT)
    oe_pin = machine.Pin(27, machine.Pin.OUT)

    # dir_pin.off()
    oe_pin.off()

def set_digit(digit, value):
    if value is None or value > 9:
        value = 0xF

    for idx, bit in enumerate(digits[digit]):
        if value & (1 << idx):
            bit.on()
        else:
            bit.off()

def set_digits(value):
    val_str = f"{value:>6}"
    
    for idx, val in enumerate(reversed(val_str)):
        if val in "0123456789":
            set_digit(idx, int(val))
        else:
            set_digit(idx, None)

initialize_pins()

while True:
    year, month, day, weekday, hour, minute, second, subsecond = rtc.datetime()
    set_digits(f"{hour:02}{minute:02}{second:02}")
    time.sleep(0.5)
