import displayController
import RPi.GPIO as GPIO
import time
import thread
import logging

# Enable debug logging into log
DEBUG = True
# Enable printing informations to std. output
VERBOSE = True

LCD_CMD = False

LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line


def debug(message):
    logging.debug(message)


def onScreen(message):
    if(VERBOSE):
        print(message)

displayTime = False


def printDateToDisplay():
    while True:
        # Display current time on display, until global variable is set
        if displayTime is True:
            thread.exit()
        timeactual = time.strftime("%d.%m. %H:%M:%S", time.localtime())
        displayController.lcd_string(timeactual, LCD_LINE_2)
        onScreen(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()))
        time.sleep(1)


def main():
    displayController.lcd_init()
    prev_input = 0
    while True:
        # displayController.lcd_string("Elija una Accion", LCD_LINE_1)
        # time.sleep(3)
        # printDateToDisplay()
        displayController.lcd_string("Ingrese una Accion", LCD_LINE_1)
        input = GPIO.input(4)
        if ((not prev_input) and input):
            displayController.lcd_string("ENTRADA: ", LCD_LINE_1)
            onScreen("Boton 1")
            printDateToDisplay()
            time.sleep(3)
        prev_input = input
        time.sleep(0.05)


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        displayController.lcd_string("Hasta Luego!", LCD_LINE_1)
        GPIO.cleanup()
