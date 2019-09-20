#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
from bluetooth import *
import bluetooth
import subprocess

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13bc
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)
listOfNames = ['HC-05', 'HC-06','DSD TECH HC-05']
listOfPrefix = ['00:14:03', '00:06:66', '98:D3:31', '20:13:04', '20:17:11', '20:18:01', '20:18:04', '20:18:07', '20:18:08', '20:18:09', '20:18:10', '20:18:11', '98:D3:35']

def main():
	counterChecks = 0
	counter = 0
	try:
		logging.info("Skimbuster v1.0 Demo")
		epd = epd2in13bc.EPD()
		logging.info("init and Clear")
		epd.init()
		time.sleep(1)
		font16 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 16)
		font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
		HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126
		HRYimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126  ryimage: red or yellow image
		drawblack = ImageDraw.Draw(HBlackimage)
		drawry = ImageDraw.Draw(HRYimage)
		drawry.text((2, 0), 'Skimbuster', font = font18, fill = 0)
		drawblack.text((175, 1), 'v1.0', font = font18, fill = 0)
		drawblack.text((35, 85), 'stutm @ SensePost', font = font16, fill = 0)
		drawblack.line((0, 20, 298, 20), fill = 0)
		drawblack.line((0, 85, 298, 85), fill = 0)
		nearby_devices = discover_devices(lookup_names = True, lookup_class = True)
		for addr, name, cod in nearby_devices:
			counter = counter + 1
			if name in listOfNames:
				deviceName = name
				counterChecks = counterChecks+1

			if(hex(cod) == '0x1f00'):
				deviceCod = hex(cod)
				counterChecks = counterChecks+1

			if addr[:8] in listOfPrefix:
				deviceMac = addr
				counterChecks = counterChecks+1


		drawblack.text((2, 20), 'Scanned devices:' + str(counter), font = font18, fill = 0)
		if(counterChecks <= 3 and counterChecks != 0):
			drawblack.text((2, 42), 'Skimmer found: '+ deviceName, font = font18, fill = 0)
			drawblack.text((2, 65), 'MAC: '+ deviceMac, font = font18, fill = 0)
		else:
			drawblack.text((2, 42), 'No skimmer found. :)', font = font18, fill = 0)
		
	
		epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
		time.sleep(20)
		logging.info("Clear...")
		epd.Clear()
		epd.sleep()
		command = "/usr/bin/sudo /sbin/shutdown -r now"
		process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
		output = process.communicate()[0]
	except IOError as e:
		logging.info(e)
	    
	except KeyboardInterrupt:    
		logging.info("ctrl + c:")
		epd2in13bc.epdconfig.module_exit()
		exit()
	

if __name__ == '__main__':
	main()
