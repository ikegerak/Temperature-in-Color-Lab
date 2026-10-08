from gpiozero import RGBLED
import time
import board
import adafruit_dht
from datetime import datetime

sensor = adafruit_dht.DHT11(board.D17) 

led = RGBLED(16, 20, 21)

def to_fahrenheit(c):
	c = float(c)
	f = round((c*(9/5)+32), 1)
	return f 

while True:
	try:
		celsius = sensor.temperature # Get the temperature in Celcius from the sensor
		fahrenheit = to_fahrenheit(celsius)
		current_time = datetime.now()
		print("{0},{1:0.1f},{2:0.1f}".format(current_time.strftime("%H:%M:%S"), celsius, fahrenheit))
		with open("temperature.csv","a") as f:
			f.write(str(current_time) + "," + str(celsius) + "," + str(fahrenheit) + "\n")

		if fahrenheit > 72:
			led.color = (1,0,0)
		else:
			led.color = (0,0,1)


		time.sleep(2.0)
	except RuntimeError as error:
		# Errors happen fairly often, DHT's are hard to read, just keep going
		print(error.args[0])
		time.sleep(2.0)
		continue
	except Exception as error:
		sensor.exit()
		raise error    
