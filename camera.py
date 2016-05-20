import picamera
import time


camera = picamera.PiCamera()
camera.rotation = 180
camera.resolution = (1024, 768)
camera.capture('/home/pi/Desktop/captura.jpg')
