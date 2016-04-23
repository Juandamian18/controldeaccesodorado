import display
import RPi.GPIO as GPIO

def main():

    try:
        while True:
            display.init
            display.lcdWriteFirstLine("Prueba")
            time.sleep(3)
