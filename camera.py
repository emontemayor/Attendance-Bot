
import qrcode
from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
sleep(5)
camera.stop_preview()

camera.start_preview(alpha=200)

code = qrcode.make('Hello World')
code.save('hellocode.png')