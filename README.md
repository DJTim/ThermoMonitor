ThermoMonitor
=============
8-Channel temperature monitor based on Raspberry Pi.

How To Install
--------------
Clone the repo to a directory. After execute following commands
```bash
$ virtualenv <directory>
$ pip install bottle
$ pip install beaker
$ pip install Jinja2
$ chmod 775 main.py
```

Run the application
```bash
$ sudo python main.py
```

Run on boot
-----------
```bash
$ crontab -e
```
add `@reboot cd <installdir>/ThermoMonitor/ && screen -dmS ThermoMonitor ./main.py`

Add custom python with root access of current python version
```bash
$ ls -l /usr/bin/python
$ sudo cp /usr/bin/python2.7 /usr/bin/pythonRoot
$ sudo chmod u+s /usr/bin/pythonRoot
```

Hardware requirements
---------------------
* 2 x ADS1115 A/D converters, one with address 0x48 the other 0x49
* 8 x AD592 temperature transducers
