import displayController
import RPi.GPIO as GPIO
import time

LCD_CMD = False

LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line


def main():
    displayController.lcd_init()
    while True:
        displayController.lcd_string("Rasbperry Pi", LCD_LINE_1)
        time.sleep(3)


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        displayController.lcd_string("Goodbye!", LCD_LINE_1)
        GPIO.cleanup()
