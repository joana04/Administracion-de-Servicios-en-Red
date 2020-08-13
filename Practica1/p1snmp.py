import rrdtool
from pysnmp.hlapi import *


def inicio ():
	cadena=""
	entra=1
	interfaces='1.3.6.1.2.1.2.1.0'
	ip="10.100.68.128"
	grupo="grupo4cm1"
	estinter='1.3.6.1.2.1.2.2.1.8'
	v=1
	nd=0
	disp=open("Dispositivos.txt","a")
	disp.close()
	print("\t\tBienvenido\n")
	disp=open("Dispositivos.txt", "r")
	#estatus(ip,grupo)
	#getInterfaces(ip,grupo,v)
	#getSI(ip,grupo,v)	
	for linea in disp:		
		cadena=linea
		nd=nd+1
	print(" ---- Dispositivos monitoreados----\n\t "+ str(nd))
	disp.close()
	disp=open("Dispositivos.txt", "r")
	for linea in disp:		
		cadena=linea.split("||")
		ip=cadena[2] 
		grupo=cadena[3]
		v=int(cadena[1])
		print("Dispositivo---> "+ cadena[0])
		estatus(cadena[2],cadena[3])
		getInterfaces(ip,grupo,v)
		getSI(ip,grupo,v)	
		#print(ip+grupo)
		
		
	disp.close()
	
	while entra==1:
		print("\nSeleccione la opcion deseada \n\t 1.- Agregar un agente \n\t 2.- Eliminar un agente \n\t 3.- Estado de dispositivo ")
		opc=int(input())
		if opc==1:
			agregarDisp()
		elif opc==2:
			eliminarDisp()
		elif opc==3:
			print ("Aun no ")
		print ("desea regresar?\n 1.-Si \n 2.-No")
		entra=int(input())
	print ("\n\t ADIOS\n")




def agregarDisp():
	print("\n\t Agregar dispositivo")
	print("Introduzca el Hostname")
	hostname=str(input())
	print("Introduzca el número de versión SNMP (1,2,3), en caso de no saberlo introduzca 0")
	ver=str(input())
	print ("Introduzca la dirección IP ")
	ip=str(input())
	print ("Introduzca la cominudad")
	com=str(input())
	print(hostname+"||"+ver+"||"+ip+"||"+com+"||"+"\n")
	disp=open("Dispositivos.txt", "a")
	disp.write(hostname+"||"+ver+"||"+ip+"||"+com+"||"+"\n")
	disp.close()

def eliminarDisp():
	print("\n\t Eliminar dispositivo")
	print("Introduzca el Hostname que desea eliminar")
	hostname=str(input())	
	nuevos=""
	disp= open("Dispositivos.txt","r")
	for linea in disp:
		cadena=linea.split("||")
		print (cadena[0] + hostname)
		if cadena[0]==hostname:
			print("Dispositivo eliminado-- Hostanme:"+cadena[0]+" SNMPv:"+cadena[1]+" IP:"+cadena[2]+" Comunidad:"+cadena[3] )
		else:
			nuevos=nuevos+linea+"\n"
	print(nuevos)
	disp.close()
	nuevo=open("Dispositivos.txt","w")
	nuevo.write(nuevos)
	nuevo.close()
	


def estatus (ip, grupo):
	print(ip+grupo)
	errorIndication, errorStatus, errorIndex, varBinds = next(
	    getCmd(SnmpEngine(),
	           CommunityData(grupo, mpModel=0),
	           UdpTransportTarget((ip, 161)),
	           ContextData(),
	           ObjectType(ObjectIdentity('1.3.6.1.2.1.1.6.0')))
	)
	if errorIndication:
		print(errorIndication)
	    #print(" Down \n")
	elif errorStatus:
		print('%s at %s' % (errorStatus.prettyPrint(),
	                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
	    #print(" Down \n")
	else:
		print("Estatus del dispositivo --> Up\n")

def getInterfaces(ip,grupo,v):
	errorIndication, errorStatus, errorIndex, varBinds = next(
	    getCmd(SnmpEngine(),
	           CommunityData(grupo, mpModel=v),
	           UdpTransportTarget((ip, 161)),
	           ContextData(),
	           ObjectType(ObjectIdentity('1.3.6.1.2.1.2.1.0')))
	)
	if errorIndication:
	    print(errorIndication)
	elif errorStatus:
	    print('%s at %s' % (errorStatus.prettyPrint(),
	                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
	else:
	    for varBind in varBinds:
	        #print(' = '.join([x.prettyPrint() for x in varBind])+"\n")
	        x=str(varBind).split("=")
	        print("Interfaces de Red--> "+ x[1]+"\n")

def getSI(ip,grupo,v):
	print ("Interface || Estatus")
	n=0
	aux=""
	for (errorIndication,
     errorStatus,
     errorIndex,
     varBinds) in nextCmd(SnmpEngine(),
                          CommunityData(grupo, mpModel=v),
                          UdpTransportTarget((ip, 161)),
                          ContextData(),
                          #0,1,
                          ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.1')),
                          ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.8')),
                          lexicographicMode=False
	
	):
		if errorIndication:
		    print(errorIndication)
		elif errorStatus:
		    print('%s at %s' % (errorStatus.prettyPrint(),
		                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
		else:
			for varBind in varBinds:
				x= str(varBind).split("=")
				n=n+1
				if n%2==0:
					if x[1]== 
					aux=aux+"          "+x[1]
					print (aux)
					print("----------||--------")
					aux=""
				else:
					aux=aux+"  "+x[1]
            
	   
inicio()