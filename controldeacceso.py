import displayController
import RPi.GPIO as GPIO

def main():
    displayController.lcd_init
    try:
        while True:
            display.lcd_string("Rasbperry Pi",LCD_LINE_1)
            time.sleep(3)
    except KeyboardInterrupt:
        GPIO.cleanup()
        pass
    GPIO.cleanup()

if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1)
    GPIO.cleanup()
