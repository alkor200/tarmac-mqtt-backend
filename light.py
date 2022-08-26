import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)


class Light:
    def __init__(self, number: int, pin: int):
        self.number = number
        self.pin = pin
        self.state = False
        self.on_since = None
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def evaluate(self):
        if self.state:
            GPIO.setup(self.pin, GPIO.HIGH)
            print("on")
        else:
            GPIO.setup(self.pin, GPIO.LOW)
            print("off")

    def turn_off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def turn_on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def toggle_state(self):
        self.state = not self.state
