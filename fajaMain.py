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


#Callbacks
def CuentaA(channel):
    global contaA
    ret,frame
    contaA += 1
    os.system("clear")
    print ("Contador A: ", contaA)
    print ("Contador B: ", contaB)
    ret,frame = cap.read()
    cv2.imshow("Entrada", frame)

def CuentaB(channel):
    global contaB
    contaB += 1
    os.system("clear")
    print ("Contador A: ", contaA)
    print ("Contador B: ", contaB)

#Interrupciones
GPIO.add_event_detect(sensorIn, GPIO.RISING, callback = CuentaA)
GPIO.add_event_detect(sensorOut, GPIO.RISING, callback = CuentaB)

print ("Contador A: ", contaA)
print ("Contador B: ", contaB)

#Bucle principal
i = 0 
while(contaA < 5):
	print(i)
	i += 1 
	time.sleep(1)

GPIO.cleanup()
cap.release()
cv2.destroyAllWindows()