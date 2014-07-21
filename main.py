import time, sys, os.path, threading, atexit, bottle
from bottle import jinja2_template as template, static_file, request, app
from bottle import response
from json import dumps

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
dataToCSV = [0, 0, 0, 0, 0, 0, 0, 0, 0]
# lock to control access to variable
dataLock = threading.Lock()
# thread handler
worker = threading.Thread()

def readAD():
	#fill list with new data
	dataToCSV[0] = time.strftime("%H:%M")

	for i in range(1, 9):
		if i < 5:
			dataToCSV[i] = round(voltToTemp(adc1.readADCSingleEnded(i-1, gain, sps)),2)
		else:
			dataToCSV[i] = i-5

def toCSV(data):
	directory = "log"
	filename = directory + "/" + time.strftime("%d%m%y%H") + ".csv"
	
	try:				#check directory existance
		os.mkdir(directory)
	except Exception:
		pass	

	out = ",".join(str(x) for x in data)	
	
	#write dataline to CSV
	with open(filename, "a") as file:
		file.write(out + "\n")

	print out

def voltToTemp(volt):
	return (volt/9.12)-273.15	#milivolt / Kelvin result is Celcius

def create_app():
    app = bottle

    def interrupt():
        global worker
        worker.cancel()

    def doWorker():
        global dataToCSV
        global worker

        with dataLock:
            readAD()
	    toCSV(dataToCSV)
	
        if runThread:
            worker = threading.Timer(POOL_TIME, doWorker, ())
            worker.start()

    def doWorkerStart():
        # If neaded do init of global vars here
        global worker
        worker = threading.Timer(0, doWorker, ())
        worker.start()

    # Initiate
    doWorkerStart()
    # When kill Bottle (SIGTERM), clear the trigger for the next thread
    atexit.register(interrupt)
    return app

web = create_app()

@web.route('/')
def index():
    return template('web/index.html');

@web.route('/api/live/')
def apiLive():
    response.content_type = 'application/json'
    return dumps(dataToCSV)

@web.route('/js/<filename:re:.*\.js>')
def javascript(filename):
    return static_file(filename, root='web/js')

@web.route('/css/<filename:re:.*\.css>')
def stylesheet(filename):
    return static_file(filename, root='web/css')

@web.route('/font/<filename:re:.*\.*>')
def fonts(filename):
    return static_file(filename, root='web/fonts')

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

