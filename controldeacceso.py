import display
import RPi.GPIO as GPIO

def main():
    try:
        while True:
            display.init
            display.lcdWriteFirstLine("Prueba")
            time.sleep(3)
    except KeyboardInterrupt:
        GPIO.cleanup()
        pass
    GPIO.cleanup()

if __name__ == '__main__':
    debug("----------========== Starting session! ==========----------")
    main()
