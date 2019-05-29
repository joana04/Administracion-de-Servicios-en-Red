import os
import threading
from time import time
from pysnmp.hlapi import *
from Hilo import Hilo
from LineaBase import EjecutarLb
from LineaBase import crearBasesLb
from clientSSH import sshClient
from clientDNS import dnsServer
from getSNMP import consultaSNMP, walkSNMP
from Rendimiento import Rendimiento
from smtp import SMTP_SENSOR
from smtp import *
from ftp_client import* 
from http_client import*
from createPdf import*


def consulta( ip, grupo, v ,pto,rendimiento):
	SO = consultaSNMP(grupo, ip ,int(pto)  ,'1.3.6.1.2.1.1.1.0')
	AT = consultaSNMP(grupo, ip ,int(pto)  ,'1.3.6.1.2.1.1.3.0')
	In = consultaSNMP(grupo, ip ,int(pto)  ,'1.3.6.1.2.1.2.1.0')
	print("SO: " + SO)
	print("AT: " + AT)
	print("In: "+In)
	rendimiento.setSO(SO)
	rendimiento.setTimeActivity(int(AT))
	rendimiento.setNumberInterfaces(int(In))



rendimiento = Rendimiento()
sensor = SMTP_SENSOR()
entra=1
print("\t\t BIENVENIDOS A LAS PRUBAS DE RENDIMIENTO\n")


while entra==1:

	hostname="Rendieminto"
	ip="10.100.77.102"
	pto="161"
	com="gr_4cm1"
	ver="1"
	tiempo_actual = time()
	ag=(hostname,
		ip,
		ver,
		pto,
		com,
		tiempo_actual)
	consulta( ip, com, ver,pto, rendimiento)
	hilo= Hilo(ag)
	#crearBasesLb(com, ip, pto,hostname)
	hilo.start()
#------------------SSH
	ssh=sshClient("192.168.122.1", "esli", "morado", 50,22, ag[4], ag[3])
	aux=ssh.split("||")
	rendimiento.setNumberConectionsSSH(aux[3])
	rendimiento.setInputTraficSSH(int(aux[1]))
	rendimiento.setOutputTraficSSH(int(aux[2]))
	rendimiento.setTimeSSH(int(aux[0]))
	rendimiento.setStatusSSH("Ready")

#---------------SMTP
	sensor.scan_smtp()
	print(sensor.imap_total)
	print(sensor.pop_total)
	rendimiento.setResponseSMTP(sensor.pop_total)
	rendimiento.setResponseIMAP(sensor.imap_total)
	rendimiento.setStatusSMTP("Ready")

	#dnsServer("localhost",53,e"xamen.tanibabys.xyz",1)
#--------------DNS

	rendimiento.setResponseDNS(dnsServer("10.100.77.61",53,"examen.tanibabys.xyz",20))
	rendimiento.setStatusDNS("Ready")

#--------FTP
	
	rendimiento.setStatusFTP("Ready")
	
	aux2=ftp_client("localhost", "usuario1", "usuario1")
	aux2=aux2.split("||")
	rendimiento.setTimeResponseFTP(aux2[0])
	rendimiento.setResponseFTP(aux2[1])


#------- HTTP
	banda = consultaSNMP(com, ip ,int(pto)  ,'1.3.6.1.2.1.2.2.1.5.1')
	
	rendimiento.setResponseHTTP(check_webserver("10.100.73.153", 80, "/index.html"))
	rendimiento.setBytesReceiveHTTP(aux[1])
	rendimiento.setSpeedDownload(banda)
	rendimiento.setStatusHTTP("Ready")

	rendimiento.setPathImageRAM("rrd/RAM.png")
	rendimiento.setPathImageHDD("rrd/HDD.png")
	rendimiento.setPathImageCPU("rrd/CPU.png")

	createPdf(rendimiento)




	"""rendimiento.setResponseSMTP(20)
	rendimiento.setResponseIMAP(23)
	rendimiento.setStatusSMTP("Ready")
	rendimiento.setResponseHTTP(200)
	rendimiento.setBytesReceiveHTTP(30)
	rendimiento.setSpeedDownload(58)
	rendimiento.setStatusHTTP("Ready")
	rendimiento.setResponseFTP(200)
	rendimiento.setTimeResponseFTP(56)
	rendimiento.setStatusFTP("Ready")
	rendimiento.setServerFileCountFTP(3)
	rendimiento.setResponseDNS(45)
	rendimiento.setStatusDNS("Ready")
	rendimiento.setNumberConectionsSSH(8)
	rendimiento.setInputTraficSSH(45)
	rendimiento.setOutputTraficSSH(89)
	rendimiento.setTimeSSH(34)
	rendimiento.setStatusSSH("Ready")
	rendimiento.setPathImageRAM("mila.jpg")
	rendimiento.setPathImageHDD("mila.jpg")
	rendimiento.setPathImageCPU("mila.jpg")
	#dnsServer("192.168.122.1",53,"google.com",1)"""


		
	print ("desea repetir el analisis?\n 1.-Si \n 2.-No")
	entra=int(input())

print ("\n\t ADIOS\n")



