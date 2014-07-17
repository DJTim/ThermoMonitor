import time, sys, os.path, threading, atexit, bottle
from bottle import jinja2_template as template, static_file, request, app

sys.path.append('Adafruit_ADS1x15')     #otherwise not possible to import lib
from Adafruit_ADS1x15 import ADS1x15

POOL_TIME = 5 #Seconds

#AD Config
ADS1015 = 0x00  # 12-bit ADC
ADS1115 = 0x01	# 16-bit ADC

gain = 6144
sps = 250

#AD Init
adc1 = ADS1x15(address= 0x48, ic=ADS1115)

# variables that are accessible from anywhere
runThread = True
dataToCSV = ["0", "0", "0", "0", "0", "0", "0", "0", "0"]
# lock to control access to variable
dataLock = threading.Lock()
# thread handler
yourThread = threading.Thread()

def readAD():
	directory = "log"
	filename = directory + "/" + time.strftime("%d%m%y%H") + ".csv"
	
	try:				#check directory existance
		os.mkdir(directory)
	except Exception:
		pass
	
	#fill list with new data
	dataToCSV[0] = time.strftime("%H:%M")

	for i in range(1, 9):
		if i < 5:
			dataToCSV[i] = "%.2f" % (voltToTemp(adc1.readADCSingleEnded(i-1, gain, sps)))
		else:
			dataToCSV[i] = "%i" %(i-5)

	out = ",".join(dataToCSV)	
	
	#write dataline to CSV
	with open(filename, "a") as file:
		file.write(out + "\n")

	print out

def voltToTemp(volt):
	return (volt/9.12)-273.15	#milivolt / Kelvin result is Celcius

def create_app():
    app = bottle

    def interrupt():
        global yourThread
        yourThread.cancel()

    def doStuff():
        global dataToCSV
        global yourThread

        with dataLock:
        # Do your stuff with commonDataStruct Here
            readAD()
        # Set the next thread to happen
        if runThread:
            yourThread = threading.Timer(POOL_TIME, doStuff, ())
            yourThread.start()

    def doStuffStart():
        # Do initialisation stuff here
        global yourThread
        # Create your thread
        yourThread = threading.Timer(POOL_TIME, doStuff, ())
        yourThread.start()

    # Initiate
    doStuffStart()
    # When kill Bottle (SIGTERM), clear the trigger for the next thread
    atexit.register(interrupt)
    return app

web = create_app()

@web.route('/')
def index():
    print dataToCSV
    return "<html><h1>%s</h1></html>" % (",".join(dataToCSV))


print "  _______ _                               __  __             _ _             "
print " |__   __| |                             |  \/  |           (_) |            "
print "    | |  | |__   ___ _ __ _ __ ___   ___ | \  / | ___  _ __  _| |_ ___  _ __ "
print "    | |  | '_ \ / _ \ '__| '_ ` _ \ / _ \| |\/| |/ _ \| '_ \| | __/ _ \| '__|"
print "    | |  | | | |  __/ |  | | | | | | (_) | |  | | (_) | | | | | || (_) | |   "
print "    |_|  |_| |_|\___|_|  |_| |_| |_|\___/|_|  |_|\___/|_| |_|_|\__\___/|_|   "
print "                                                                             "
print "                                                                             "

web.run(host='0.0.0.0', port=8080, debug=False)
runThread = False

