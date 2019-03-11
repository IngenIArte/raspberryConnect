import os
import RPi.GPIO as GPIO  
import threading
import time

import cv2
cap = cv2.VideoCapture(0)
#Para sensores se va a usar los pines 11(GPIO.17) y 12(GPIO.18)

sensorIn 	= 	17 #SensorTouch en prueba
sensorOut 	= 	18 #SensorEncoder en 

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensorIn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sensorOut, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

valorSensorIn = GPIO.input(sensorIn)


print(valorSensorIn)




contaA = 0
contaB = 0

#----------------------------Funciones---------------------------------------------------------------
def detectarCirculo(image_np):
	global contaA
	ipCamQueue = contaA
	image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
	print ("ingreso")
	frameROI = image_np[44:332, 33:459]
	#hsv = cv2.cvtColor(frameROI, cv2.COLOR_BGR2GRAY)
	threshold = cv2.adaptiveThreshold(frameROI,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,9)

	#img = cv2.medianBlur(img,5)
	cimg = cv2.cvtColor(frameROI,cv2.COLOR_GRAY2BGR)
	ROI = cv2.cvtColor(frameROI,cv2.COLOR_GRAY2BGR)
	circles = cv2.HoughCircles(threshold,cv2.HOUGH_GRADIENT,1,20,
                                param1=11, param2=20, minRadius=15, maxRadius=50)

	print(type(circles))
	try: 
		hayCircle = len(circles[0,:])
	except:
		hayCircle = 0

	#cv2.imwrite("imagen.png", image_np)
	if hayCircle == 0:
		print("es None")

	else:
		circles = np.uint16(np.around(circles))
		print("circulos",circles)
		for i in circles[0,:]:
			# draw the outer circle
			print(i[0],i[1],i[2])
			if i[0] > 250 and i[0] < 450 and i[1] > 40 and i[1] < 180:
				cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
				# draw the center of the circle
				x = i[0]
				y = i[1]
				w = i[0] - 250
				if w < 0:
					w = 0
				h = i[1] + 100
				cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
				cv2.rectangle(cimg,(x,y),(w,h),(255,0,0),1)
				ROI = threshold[y:h-y+120,w:x-w+200]
				ROIDraw = frameROI[y:h-y+120,w:x-w+200]

				_, contours0, hierarchy = cv2.findContours(ROI,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
				area  =  []

				j  = 0
				for cnt in contours0:
					area.append(cv2.contourArea(cnt))
					if cv2.contourArea(cnt) > 1:
						M = cv2.moments(cnt)
						#print("Momento", M)
						cx = int(M['m10']/M['m00'])
						cy = int(M['m01']/M['m00'])
						if cx > 20 and cx < 100:
							#print(cx,cy)
							j += 1
						
						cv2.circle(ROIDraw,(cx,cy), 5, (0,0,255), -1)

				print("total", j)
				if j < 12:
					tamano = len(ipCamQueue)
					cantidadX = 5 - tamano

					enviaDato  = 's' + (cantidadX*'x') + ipCamQueue + 'a'
					print("envia:", enviaDato)

		#pixelValue = ROI[14,49]
		dim = ROI.shape
		print(dim)
		#print("Valor de pixel", pixelValue)
		cv2.imshow('detected circles',cimg)
                        
#-----------------------------Funciones para interrupcion-------------------------------------------
def CuentaA(channel):
    global contaA
    contaA += 1
    os.system("clear")
    print ("Contador A: ", contaA)
    print ("Contador B: ", contaB)
    ret, frame = cap.read()
    detectarCirculo(frame)
    cv2.imshow("Entrada", frame)
    nombreCuenta = "im" + str(contaA) + ".jpg"
    cv2.imwrite(nombreCuenta, frame)

def CuentaB(channel):
    global contaB
    contaB += 1
    os.system("clear")
    print ("Contador A: ", contaA)
    print ("Contador B: ", contaB)

#Interrupciones
GPIO.add_event_detect(sensorIn, GPIO.RISING, callback = CuentaA)
GPIO.add_event_detect(sensorOut, GPIO.RISING, callback = CuentaB)

#print ("Contador A: ", contaA)
#print ("Contador B: ", contaB)

#Bucle principal
i = 0 
while(contaA < 5):
	print(i)
	i += 1 
	time.sleep(1)
GPIO.cleanup()
cap.release()
cv2.destroyAllWindows()