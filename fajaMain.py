import RPi.GPIO as GPIO  

#Para sensores se va a usar los pines 11(GPIO.17) y 12(GPIO.18)

sensorIn 	= 	17
sensorOut 	= 	18

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensorIn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sensorOut, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

valorSensorIn = GPIO.input(sensorIn)


print(valorSensorIn)