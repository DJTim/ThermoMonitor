import time, signal, sys, os.path

sys.path.append('Adafruit_ADS1x15')     #otherwise not possible to import lib
from Adafruit_ADS1x15 import ADS1x15

#AD Config
ADS1015 = 0x00  # 12-bit ADC
ADS1115 = 0x01	# 16-bit ADC

gain = 6144
sps = 250

#AD Init
adc1 = ADS1x15(address= 0x48, ic=ADS1115)

def readAD():
	directory = "log"
	t = time.strftime("%H:%M")
	filename = directory + "/" + time.strftime("%d%m%y%H") + ".csv"
	
	try:				#check directory existance
		os.mkdir(directory)
	except Exception:
		pass

	ch1 = adc1.readADCSingleEnded(0, gain, sps)
	ch2 = adc1.readADCSingleEnded(1, gain, sps)
	ch3 = adc1.readADCSingleEnded(2, gain, sps)
	ch4 = adc1.readADCSingleEnded(3, gain, sps)
	
	out = "%s,%.2f,%.2f,%.2f,%.2f" % (t,voltToTemp(ch1),voltToTemp(ch2),voltToTemp(ch3),voltToTemp(ch4))

	with open(filename, "a") as file:
		file.write(out + "\n")

	print out

def voltToTemp(volt):
	return (volt/9.12)-273.15	#milivolt / Kelvin result is Celcius

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
