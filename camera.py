import picamera
import time


def camera_capturar(mensaje):
    camera = picamera.PiCamera()
    camera.rotation = 180
    camera.resolution = (600, 600)
    camera.start_preview()
    time.sleep(1)
    camera.capture('/home/pi/Desktop/imagen-%s.jpg' % mensaje)
    camera.stop_preview()
