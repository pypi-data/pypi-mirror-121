from transformar import four_point_transform
#from imutils.perspective import four_point_transform
from contornos import sort_contours
import numpy as np
import argparse
import imutils
import cv2
import pytesseract
import pyttsx

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # permite invocar tesseract desde python

imagen = cv2.imread('foto4.jpg')  # se carga la imagen

escalaGrises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)  # convierte a escala de grises
suavizado = cv2.GaussianBlur(escalaGrises,(5,5),0)
umbral = cv2.adaptiveThreshold(escalaGrises, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 91, 11)

bordes = cv2.Canny(suavizado, 75, 200)
#===========================CONTORNOS====================================

cnts = cv2.findContours(bordes.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
docCnt = None

#==============================
if len(cnts) > 0:
	# sort the contours according to their size in
	# descending order
	cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
	# loop over the sorted contours
	for c in cnts:
		# approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
		# if our approximated contour has four points,
		# then we can assume we have found the paper
		if len(approx) == 4:
			docCnt = approx
			break
hoja = four_point_transform(escalaGrises, docCnt.reshape(4, 2))
warped = four_point_transform(escalaGrises, docCnt.reshape(4, 2))

#===========================Umbral adaptivo====================================


thresh = cv2.threshold(warped, 0, 255,
	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]



#=====================================================================C===

#grados de precision  thres ->
texto = pytesseract.image_to_string(hoja)
print(texto)

engine = pyttsx.init('espeak')
engine.setProperty('rate', 175)
#voices = engine.getProperty('voices')
#engine.setProperty('voice', voices[1].id)
engine.say(texto)
engine.runAndWait()



"""
#cv2.imshow("1 umbral", umbral)
cv2.imshow("2 warped+thres", thresh)
cv2.imshow("3-warped", warped)
cv2.imshow("4-hoja", hoja)
"""

cv2.waitKey(0)
