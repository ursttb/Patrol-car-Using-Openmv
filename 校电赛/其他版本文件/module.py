from pyb import Pin
import time

class Buzz:
    def __init__(self, pin):
        self.Buzz_pin = Pin(pin, Pin.OUT)

    def Buzzer_Start(self):
        self.Buzz_pin.low()
        time.sleep(10)
        self.Buzz_pin.high()

## 使用示例
#buzz = Buzz('P9')
#buzz.Buzzer_Start()
