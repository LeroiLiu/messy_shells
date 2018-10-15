#coding:utf-8
from pymouse import *
import pyHook

import serial
import serial.tools.list_ports

plists = list(serial.tools.list_ports.comports())
if len(plists) <= 0:
    print("the serial port can't find")
else:
	if len(plists)==1 and list(plists[0])[0]=="COM1":
		print("the serial port can't find")
	else:
		print("the serial ports available are follows:")
		compose = ''
		for plist in plists:
			port = list(plist)
			serialName = port[0]
			if serialName!="COM1":
				print(serialName)
				compose += serialName.replace("COM","")+" "
		aflag = False
		while aflag==False:
			aport = raw_input("please type the serial number like "+compose+":")
			try:
				serialFd = serial.Serial("COM"+aport, 115200, timeout=60)
				if serialFd:
					print("check which[%s] port was really used>" % serialFd.name)
					aflag=True
			except Exception as e:
				print("there is something wrong with your input,please check and try it again")


		m = PyMouse()
		m.position()
		x_dim, y_dim = m.screen_size()
		data = serialFd.write("width:"+str(x_dim)+",height:"+str(y_dim))
		while True:
		    reces = serialFd.readline().replace(' ','').replace("\n","").replace("\r","").split(',')
		    for rece in reces:
		    	xy = rece.split(':')
		    	if xy[0]=='x':
		    		try:
		    			x_m = int(xy[1])
		    		except Exception as e:
		    			x_m = -1
		    		if x_m>x_dim or x_m<0:
		    			x_m = -1
		    	elif xy[0]=='y':
		    		try:
		    			y_m = int(xy[1])
		    		except Exception as e:
		    			y_m = -1
		    		if y_m>y_dim or y_m<0:
		    			y_m = -1

		    if x_m>=0 and y_m>=0:
		    	m.move(x_m, y_m)


