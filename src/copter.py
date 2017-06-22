import time
import lib.BMP085 as BMP085

sensor = BMP085.BMP085()

try:
	while True:
		print "Temp" + str(sensor.readTemperature())

		time.sleep(1)

except KeyboardInterrupt:
	print "End.."


