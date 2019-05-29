#from Graficar import Ejecutar
import os, time
import threading
from pysnmp.hlapi import *
from LineaBase import EjecutarLb
from LineaBase import crearBasesLb

#from smtp import *

class Hilo(threading.Thread):
	def __init__(self,ag):
		threading.Thread.__init__(self, target=Hilo.run)
		self.ag=ag
		self.stopRequest = threading.Event()
		self.inicio=""
		self.fin=""
		self.ban=0
		self.unaVez=0
		


	def run(self):
		while not self.stopRequest.isSet():
			try:
				#Ejecutar(self.ag[4], self.ag[1], self.ag[3], self.ag[0], self.ag[5])
				
				#EjecutarMc(self.ag[4], self.ag[1], self.ag[3], self.ag[0], self.ag[5], self.ag[6])
				#time.sleep(1)
				print("Estoy en el hilo")
				EjecutarLb( self.ag[4], self.ag[1], self.ag[3], self.ag[0], self.ag[5])
				#EjecutarP(self, self.ag[4], self.ag[1], self.ag[3], self.ag[0])
				
				
				time.sleep(1)
			except Exception as e:
				print(e)
				time.sleep(2)
			continue
	
	def join(self, timeout = None):
		self.stopRequest.set()
		#super(Monitor, self).join(timeout)

 

