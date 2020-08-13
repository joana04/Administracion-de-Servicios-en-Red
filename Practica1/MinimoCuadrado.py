import rrdtool , time , os , errno
from getSNMP import consultaSNMP
from os.path import basename
from notify import sendAlertEmail

lbPathmc = os.getcwd() + "/rrd/minimosCuadrados/"

def creaeBasesMC(comunidad, ip, port, name):
	
	agentPath = lbPathmc + name + "/"
	try:
		os.makedirs(os.path.dirname(agentPath))
	except OSError as exc:
		if exc.errno != errno.EEXIST:
			print("Error de directorios: minimosCuadrados.")
			raise
	ret = rrdtool.create(agentPath + name + "trend.rrd",
		"--start", 'N',
		"--step", '60',
		"DS:CPUload:GAUGE:600:U:U",
		"RRA:AVERAGE:0.5:1:24"
	)

	if ret:
		print(rrdtool.error())

def EjecutarMc(comunidad, ip, port, name, times, umbral ):

	if name=='linux'or name=="linuxmario":
		carga_CPU = int(consultaSNMP(comunidad , ip , port ,'1.3.6.1.2.1.25.3.3.1.2.196608'))
	elif name=="examen":
		carga_CPU = int(consultaSNMP(comunidad , ip , port ,'1.3.6.1.2.1.25.3.3.1.2.769'))
	else:
		carga_CPU = int(consultaSNMP(comunidad , ip , port ,'1.3.6.1.2.1.25.3.3.1.2.3'))
	agentPath = lbPathmc + name + "/"
	#carga_CPU = int(consultaSNMP(comunidad , ip , port ,'1.3.6.1.2.1.25.3.3.1.2.196608'))
	valor = "N:" + str(carga_CPU)
	time.sleep(1)


	rrdtool.update(str(agentPath + str(name)) + 'trend.rrd', valor)

	tiempo_final = int(rrdtool.last(agentPath + str(name) + "trend.rrd"))
	tiempo_inicial = tiempo_final - 3600

	ret2 = rrdtool.graphv(  str(agentPath + name)+"deteccion.png",
                     "--start",str(tiempo_inicial),
                     "--end",str(tiempo_final+15500),
                    "--title","Carga de CPU",
                     "--vertical-label=Uso de CPU (%)",
                    '--lower-limit', '0',
                    '--upper-limit', '100',
                     "DEF:carga="+ agentPath + name + "trend.rrd:CPUload:AVERAGE",
                     "CDEF:umbral25=carga,"+str(umbral)+",LT,0,carga,IF",
                     "VDEF:cargaMAX=carga,MAXIMUM",
                     "VDEF:cargaMIN=carga,MINIMUM",
                     "VDEF:cargaSTDEV=carga,STDEV",
                     "VDEF:cargaLAST=carga,LAST",
                     "AREA:carga#00FF00:Carga del CPU",
                     "AREA:umbral25#FF9F00:Tráfico de carga mayor que"+str(umbral),
                     "HRULE:"+str(umbral)+"#FF0000:"+str(umbral)+"%",
                     "GPRINT:cargaMIN:%6.2lf %SMIN",
                     "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                     "GPRINT:cargaLAST:%6.2lf %SLAST",
                     # ---METODO DE MINIMOS CUADRADOS
					 "VDEF:m=carga,LSLSLOPE",
					 "VDEF:b=carga,LSLINT",
					 'CDEF:avg2=carga,POP,m,COUNT,*,b,+',
					 "LINE2:avg2#FFBB00",
					 #'VDEF:um=m,0,LT,90,0,IF'
					 #'VDEF:um2=um,100,LT,0,90,0,IF'
					 'CDEF:abc=avg2,'+str(umbral)+','+str(umbral+ 100000000)+',LIMIT',
					 'CDEF:abc2=avg2,-10,0,LIMIT',
					
					 'VDEF:primero=abc,FIRST',
					 'VDEF:primero2=abc2,FIRST',
					 "GPRINT:primero:  Alcanzara el umbral "+ str(umbral)+"%  @ %c :strftime",
					 "GPRINT:primero2:  Alcanzara el umbral  0% @ %c :strftime",
					 "PRINT:primero: Alcanzara umbral el @ %c :strftime",
					 "PRINT:cargaLAST:%6.2lf %S "
			)

	alcanza_umbral=ret2['print[0]']
	
	ultimo_valor= ret2['print[1]']
	
	#print ("alcanza umbral"+ str(alcanza_umbral)+str(ultimo_valor))
	#valores= ultimo_valor.split(" ")
	#print (ultimo_valor + alcanza_umbral)
	#print("Archivo generado en " + str(agentPath + name)+"deteccion.png")

	if float(ultimo_valor)>int(umbral):
		sendAlertEmail("Agente "+name+" sobrepasó umbral de minimos cuadrados"+str(ultimo_valor), str(agentPath + name)+"deteccion.png",str(agentPath + str(name)) + 'trend.rrd')
	elif( float(ultimo_valor)==0):
		sendAlertEmail("Agente "+name+" sobrepasó umbral 0 de minimos cuadrados"+str(ultimo_valor), str(agentPath + name)+"deteccion.png",str(agentPath + str(name)) + 'trend.rrd')
	

