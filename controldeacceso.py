import displayController
import RPi.GPIO as GPIO
import time
import thread
import logging
import mysql
import picamera
import MFRC522


# Enable debug logging into log
DEBUG = True
# Enable printing informations to std. output
VERBOSE = True

LCD_CMD = False

LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
camera = picamera.PiCamera()


class Actions:
    entrada=1
    salida=2


def readNfc():
    reading = True
    while reading:
        MIFAREReader = MFRC522.MFRC522()

        # while continue_reading:
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        if status == MIFAREReader.MI_OK:
            print("Card detected")

        (status, backData) = MIFAREReader.MFRC522_Anticoll()
        if status == MIFAREReader.MI_OK:
            # print ("Card Number: "+str(backData[0])+","+str(backData[1])+","+str(backData[2])+","+str(backData[3])+","+str(backData[4]))
            MIFAREReader.AntennaOff()
            reading = False
            return str(backData[0]) + str(backData[1]) + str(backData[2]) + str(backData[3]) + str(backData[4])


def ledRedOn():
    GPIO.output(19, True)

def ledRedOff():
    GPIO.output(19, False)

def camera_capturar(mensaje):
    camera.rotation = 180
    camera.resolution = (600, 600)
    camera.start_preview()
    time.sleep(1)
    camera.capture('/home/pi/Desktop/imagen-%s.jpg' % mensaje)
    camera.stop_preview()


def readNfc1(action):
    if(action == 1):
        displayController.lcd_string("ENTRADA: ", LCD_LINE_1)
        onScreen("Entrada...")
        displayController.lcd_string("Acerque Tarjeta", LCD_LINE_2)
        dataRFID = readNfc()
        displayController.lcd_string("Codigo Tarjeta:", LCD_LINE_1)
        displayController.lcd_string(dataRFID, LCD_LINE_2)
        time.sleep(2)
        mysql.insertReading(dataRFID, Actions.entrada)
        displayController.lcd_string("Mire a la Camara", LCD_LINE_1)
        displayController.lcd_string("", LCD_LINE_2)
        camera_capturar(time.strftime("%d-%m-%Y %H-%M-%S", time.localtime()))
        displayController.lcd_string("Ingreso Exitoso!", LCD_LINE_1)
        displayController.lcd_string("", LCD_LINE_2)
        time.sleep(2)
    if(action == 2):
        displayController.lcd_string("SALIDA: ", LCD_LINE_1)
        onScreen("Salida...")
        displayController.lcd_string("Acerque Tarjeta", LCD_LINE_2)
        dataRFID = readNfc()
        displayController.lcd_string("Codigo Tarjeta:", LCD_LINE_1)
        displayController.lcd_string(dataRFID, LCD_LINE_2)
        time.sleep(2)
        mysql.insertReading(dataRFID, Actions.salida)
        displayController.lcd_string("Mire a la Camara", LCD_LINE_1)
        displayController.lcd_string("", LCD_LINE_2)
        camera_capturar(time.strftime("%d-%m-%Y %H-%M-%S", time.localtime()))
        displayController.lcd_string("Ingreso Exitoso!", LCD_LINE_1)
        displayController.lcd_string("", LCD_LINE_2)
        time.sleep(2)

    # Sleep a little, so the information about last action on display is read
    time.sleep(1)


def debug(message):
    logging.debug(message)


def onScreen(message):
    if(VERBOSE):
        print(message)

displayTime = False


def printDateToDisplay():
    while True:
        # Display current time on display, until global variable is set
        if displayTime is False:
            thread.exit()
        displayController.lcd_string(time.strftime("%d.%m. %H:%M:%S", time.localtime()), LCD_LINE_2)
        onScreen(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()))
        time.sleep(60)


def main():
    GPIO.cleanup()
    displayController.lcd_init()
    prev_input_entrada = 0
    prev_input_salida = 0
    while True:
        displayController.lcd_string("Elija una Accion", LCD_LINE_1)
        displayController.lcd_string("Ingreso   Salida", LCD_LINE_2)
        inputentrada = GPIO.input(4)
        inputsalida = GPIO.input(3)
        # Boton ENTRADA presionado
        if ((not prev_input_entrada) and inputentrada):
            readNfc1(1)
        prev_input_entrada = inputentrada
        time.sleep(0.05)
        # Boton SALIDA presionado
        if ((not prev_input_salida) and inputsalida):
            readNfc1(2)
        prev_input_salida = inputsalida
        time.sleep(0.05)


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        displayController.lcd_string("Hasta Luego!", LCD_LINE_1)
        displayController.lcd_string("", LCD_LINE_2)
        GPIO.cleanup()
