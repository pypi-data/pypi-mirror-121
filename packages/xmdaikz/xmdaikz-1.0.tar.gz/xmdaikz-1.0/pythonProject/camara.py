from gpiozero import Button
from picamera import PiCamera
from signal import pause

boton = Button(3)
camara = PiCamera()


def capturar():
    camara.capture('foto.jpg')


boton.when_pressed = capturar

pause()
