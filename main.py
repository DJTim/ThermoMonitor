import time, signal, sys

sys.path.append('Adafruit_ADS1x15')     #otherwise not possible to import lib
from Adafruit_ADS1x15 import ADS1x15

#AD Config
ADS1015 = 0x00  # 12-bit ADC
ADS1115 = 0x01	# 16-bit ADC

gain = 4096
sps = 250

#AD Init
adc = ADS1x15(ic=ADS1115)

def readAD():
	t = time.strftime("%H:%M")
	filename = time.strftime("%d%m%y%H") + ".csv"
	
	ch1 = adc.readADCSingleEnded(0, gain, sps) / 1000
	ch2 = adc.readADCSingleEnded(1, gain, sps) / 1000
	ch3 = adc.readADCSingleEnded(2, gain, sps) / 1000
	ch4 = adc.readADCSingleEnded(3, gain, sps) / 1000
	
	out = "%s,%.6f,%.6f,%.6f,%.6f" % (t, ch1, ch2, ch3, ch4)	

	with open(filename, "a") as file:
		file.write(out + "\n")

	print out

def loop():
	try:
		while True:
			readAD()
			time.sleep(60)
	except KeyboardInterrupt:
		sys.exit()

print "ThermoMomitor"
print "Ctrl + C to stop"
loop()
