import os, time
import threading
from Graficar import*
from pysnmp.hlapi import *

class Hilo(threading.Thread):
	def __init__(self, hostname, ip, grupo, time,pto):
		super(Hilo, self).__init__()
		self.agent = hostname
		self.ip=ip
		self.grupo=grupo
		self.port= pto
		self.time=time
		self.stopRequest = threading.Event()

		def run(self):
			while not self.stopRequest.isSet():     
				try:
					Ejecutar( self.grupo, self.ip, self.port , self.hostname , self.time)   
					time.sleep(1)
						
				except Exception as e:
					print(e.message)
					time.sleep(2)		
				continue
			