import displayController
import RPi.GPIO as GPIO

def main():

    try:
        displayController.lcd_init
        while True:
            displayController.lcd_string("Prueba",LCD_LINE_1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        pass
    GPIO.cleanup()
