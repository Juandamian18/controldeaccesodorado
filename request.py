import requests

url = 'http://192.168.1.11/sistema-moteles/test'
files = {'captura': open('/home/pi/Desktop/captura.jpg', 'rb')}

r = requests.post(url, files=files)
print r.text
