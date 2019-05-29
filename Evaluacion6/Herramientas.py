import rrdtool
import  time
from pysnmp.hlapi import *
from getSNMP import consultaSNMP, walkSNMP

def estatus ( ip, grupo):
	errorIndication, errorStatus, errorIndex, varBinds = next(
		getCmd(SnmpEngine(),
			   CommunityData(grupo, mpModel=0),
			   UdpTransportTarget((ip, 161)),
			   ContextData(),
			   ObjectType(ObjectIdentity('1.3.6.1.2.1.1.6.0')))
	)
	if errorIndication:
		print(" Down \n")
		return 0
	elif errorStatus:
		
		print(" Down \n")
		return 0
	else:
		print("Estatus del dispositivo --> Up\n")
		return 1

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
				xn=int(x[1])
				n=n+1
				if n%2==0:
					if xn== 1:
						aux=aux+"          "+"up"
					elif x[1]=="2":
						aux=aux+"        "+"down"
					else:
						aux=aux+"        "+ "testing"
					print (aux)
					print("----------||--------")
					aux=""
				else:
					aux=aux+"  "+x[1]
def getsnmp(ip,grupo,v, oid,pto):
	errorIndication, errorStatus, errorIndex, varBinds = next(
		getCmd(SnmpEngine(),
			   CommunityData(grupo, mpModel=v),
			   UdpTransportTarget((ip, pto)),
			   ContextData(),
			   ObjectType(ObjectIdentity(oid)))
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
			#print("Interfaces de Red--> "+ x[1]+"\n")
			return x[1]

def inventario( ip, comunidad ):
	print ("Creando inventario")	
	v=1
	disp= open("Inventario.txt","a")
	disp.write("Router: "+ip+"\n")
	hola=getsnmp(ip,comunidad,v, "1.3.6.1.2.1.1.1.0", 161 )
	disp.write("SO: "+getsnmp(ip,comunidad,v, "1.3.6.1.2.1.1.1.0", 161 )+"\n")
	disp.write("Ubicación físia: "+getsnmp(ip,comunidad,v, '1.3.6.1.2.1.1.6.0', 161 )+"\n")
	disp.write("Contacto: "+getsnmp(ip,comunidad,v, '1.3.6.1.2.1.1.4.0', 161 )+"\n")
	disp.write("Interfaces: "+getsnmp(ip,comunidad,v, '1.3.6.1.2.1.2.1.0', 161 )+"\n")
	disp.write("Carga CPU: "+consultaSNMP(comunidad , ip , 161 ,'1.3.6.1.2.1.25.3.3.1.2.768')+"\n")
	disp.write("RAM: "+consultaSNMP(comunidad, ip, 161, '1.3.6.1.2.1.25.2.3.1.5.1')+"\n")
	disp.write("HDD: "+consultaSNMP(comunidad, ip, 161, '1.3.6.1.2.1.25.2.3.1.5.36')+"\n\n")
	disp.write("-------------------------------------------------------------------------\n\n")
	disp.close()

#inventario("192.168.232.1", "redes3")