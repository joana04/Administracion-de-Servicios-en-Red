import rrdtool, time, os, errno
from getSNMP import consultaSNMP, walkSNMP


lbPath = os.getcwd() +"/rrd/"


def crearBasesLb(comunidad, ip, port, name):
	agentPath = lbPath   + "/"
	try:
		os.makedirs(os.path.dirname(agentPath))
	except OSError as exc:
		if exc.errno != errno.EEXIST:
			print("Error de directorios: Linea Base.")
			raise

	# 1 BD Trafico de RAM
	ret = rrdtool.create(agentPath + "RAM.rrd",
		"--start", 'N',
		"--step", '60',
		"DS:RAMusado:GAUGE:600:U:U",
		"DS:RAMtotal:GAUGE:600:U:U",
		"RRA:AVERAGE:0.5:1:24",
		"RRA:AVERAGE:0.5:1:24"
	)

	if ret:
		print(rrdtool.error())

	# 2 BD Trafico de CPU


	ret = rrdtool.create(agentPath + "CPU.rrd",
			"--start", 'N',
			"--step", '60',
			"DS:CPUload:GAUGE:600:U:U",
			"RRA:AVERAGE:0.5:1:24"
	)

	if ret:
			print(rrdtool.error())

	# 3 BD Trafico de HDD
	ret = rrdtool.create(agentPath + "HDD.rrd",
		"--start", 'N',
		"--step", '60',
		"DS:HDDusado:GAUGE:600:U:U",
		"DS:HDDtotal:GAUGE:600:U:U",
		"RRA:AVERAGE:0.5:1:24"
	)

	if ret:
		print(rrdtool.error())






def EjecutarLb( comunidad, ip, port, name, times):
	agentPath = lbPath   + "/"

		# 1 RAM de interfaz
	ramUsada = int(consultaSNMP(comunidad, ip, port, '1.3.6.1.2.1.25.2.3.1.6.1'))
	ramTotal = int(consultaSNMP(comunidad, ip, port, '1.3.6.1.2.1.25.2.3.1.5.1'))
	
	valor = "N:" + str(ramUsada) + ':' + str(ramTotal)

	rrdtool.update(str(agentPath ) + 'RAM.rrd', valor)

# 1 Grafica RAM de interfaz
	finalTime = int(rrdtool.last(str(agentPath ) + "RAM.rrd"))
	initialTime = finalTime - 3600

	ret = rrdtool.graphv(
			str(agentPath ) + "RAM.png",
			"--start", str(initialTime),
			"--vertical-label=Carga RAM",
			"--title=USO DE RAM - LINEA DE BASE",
			"--color", "ARROW#009900",
			'--vertical-label', "Uso de RAM (%)",
			'--lower-limit', '0',
			'--upper-limit', '100',
			"DEF:usada=" + str(agentPath ) + "RAM.rrd:RAMusado:AVERAGE",
			"DEF:total=" + str(agentPath ) + "RAM.rrd:RAMtotal:AVERAGE",
			"CDEF:porciento=usada,100,*,total,/",
			
			"VDEF:cargaSTDEV=usada,STDEV",

			"GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
			
			"AREA:porciento#00FF00:RAM Storage",
			'VDEF:ultimo=porciento,LAST',

			"VDEF:RAMlast=porciento,LAST",
			"VDEF:RAMmin=porciento,MINIMUM",
			"VDEF:RAMavg=porciento,AVERAGE",
			"VDEF:RAMmax=porciento,MAXIMUM",
			"VDEF:RAMmax2=porciento,STDEV",
			"CDEF:aux=porciento,5,+",
			"CDEF:aux2=porciento,2,+",
			"VDEF:RAMavg2=aux,AVERAGE",
			"VDEF:RAMavg3=aux2,AVERAGE",



			"HRULE:RAMavg2#BB0000:Umbral Go",
			"HRULE:RAMavg3#00BB00:Umbral Set",
			"HRULE:RAMavg#000000:Umbral Ready",

			"CDEF:umbral25=porciento,RAMavg2,LT,0,porciento,IF",
			"AREA:umbral25#FF9F00:Tráfico de carga mayor que umbral 3",
			
			#'CDEF:abc=porciento,RAMavg,100,LIMIT',
			"PRINT:ultimo:%12.0lf%s",
			"PRINT:RAMavg2:%12.0lf%s ",
			

			"COMMENT:        Last              Now             Min                 Avg               Max//n",
			"GPRINT:RAMlast:%12.0lf%s",
			"GPRINT:RAMmin:%10.0lf%s",
			"GPRINT:RAMavg:%13.0lf%s",
			"GPRINT:RAMmax:%13.0lf%s",
			
	)
	
	#ultimo_valor= float(ret['print[0]'])
	#limite= float(ret['print[1]'])

	#print (ultimo_valor )

	#valores= ultimo_valor.split(" ")
	#lim=limite.split(" ")
	#print (name+"RAM--valor" +str(ultimo_valor) + "limite "+ str(limite))
	#if float(ultimo_valor)>float(limite):
	#	sendAlertEmail("Agente "+name+"Sobrepasó umbral RAM Go con :"+str(ultimo_valor), str(agentPath  ) +"RAM.png",str(agentPath  ) + "RAM.rrd")
	


	
			
	#-----------------------------------------------------------------------------------------
	# 2 CPU de interfaz
	
	
	#if name=='linux'or name=="linuxmario":
	carga_CPU = int(consultaSNMP(comunidad , ip , port ,'1.3.6.1.2.1.25.3.3.1.2.196608'))
	#elif name=="examen":
	#	carga_CPU = int(consultaSNMP(comunidad , ip , port ,'1.3.6.1.2.1.25.3.3.1.2.769'))
	#else:
	#	carga_CPU = int(consultaSNMP(comunidad , ip , port ,'1.3.6.1.2.1.25.3.3.1.2.3'))

	#carga_CPU = int(consultaSNMP(comunidad , ip , port ,'1.3.6.1.2.1.25.3.3.1.2.196608'))
	valor = "N:" + str(carga_CPU)
	time.sleep(1)

	rrdtool.update(str(agentPath ) + 'CPU.rrd', valor)

	tiempo_final = int(rrdtool.last(str(agentPath ) + "CPU.rrd"))
	tiempo_inicial = tiempo_final - 3600

	ret2 = rrdtool.graphv(  str(agentPath  ) +"CPU.png",
                     "--start",str(tiempo_inicial),
                     "--end",str(tiempo_final+1000),
                    "--title","Carga de CPU",
                     "--vertical-label=Uso de CPU (%)",
                    '--lower-limit', '0',
                    '--upper-limit', '100',
                     "DEF:carga="+ str(agentPath  ) + "CPU.rrd:CPUload:AVERAGE",
                    # "CDEF:umbral25=carga,"+str(umbral)+",LT,0,carga,IF",
                     "VDEF:cargaMAX=carga,MAXIMUM",
                     "VDEF:cargaMIN=carga,MINIMUM",
                     "VDEF:cargaSTDEV=carga,STDEV",
                     "VDEF:cargaLAST=carga,LAST",
                     "AREA:carga#00FF00:Carga del CPU",
                    
                    # "HRULE:"+str(umbral)+"#FF0000:"+str(umbral)+"%",
                     "GPRINT:cargaMIN:%6.2lf %SMIN",
                     "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                     "GPRINT:cargaLAST:%6.2lf %SLAST",

                     # ---METODO DE MINIMOS CUADRADOS
					 #"VDEF:m=carga,LSLSLOPE",
					 #"VDEF:b=carga,LSLINT",
					 #'CDEF:avg2=carga,POP,m,COUNT,*,b,+',
					 #"LINE2:avg2#FFBB00",
					 #'VDEF:um=m,0,LT,90,0,IF'
					 #'VDEF:um2=um,100,LT,0,90,0,IF'
					"VDEF:CPUavg=carga,AVERAGE",
					"CDEF:aux=carga,5,+",
					"CDEF:aux2=carga,2,+",
					"VDEF:CPUavg2=aux,AVERAGE",
					"VDEF:CPUavg3=aux2,AVERAGE",



					"HRULE:CPUavg2#BB0000:Umbral Go",
					"HRULE:CPUavg3#00BB00:Umbral Set",
					"HRULE:CPUavg#000000:Umbral Ready",

					"CDEF:umbral25=carga,CPUavg2,LT,0,carga,IF",
					"AREA:umbral25#FF9F00:Tráfico de carga mayor que CPUavg2",
					
					"AREA:umbral25#FF9F00:Tráfico de carga mayor que umbral 3",

					# 'CDEF:abc=avg2,'+str(umbral)+','+str(umbral+ 100000000)+',LIMIT',
					# 'CDEF:abc2=avg2,-10,0,LIMIT',
					
					 #'VDEF:primero=abc,FIRST',
					 #'VDEF:primero2=abc2,FIRST',
					 #"GPRINT:primero:  Alcanzara el umbral "+ str(umbral)+"%  @ %c :strftime",
					 #"GPRINT:primero2:  Alcanzara el umbral  0% @ %c :strftime",
					 #"PRINT:primero: Alcanzara umbral el @ %c :strftime",
					 "PRINT:cargaLAST:%6.2lf %S ",
					 "PRINT:CPUavg2:%6.2lf %S "
			)

	#alcanza_umbral=ret2['print[0]']
	
	#ultimo_valor= ret2['print[0]']
	#limite= ret2['print[1]']
	#print (ultimo_valor + limite)

	#if float(ultimo_valor)>float(limite):
	#	sendAlertEmail("Evidencia 3  Equipo2 Grupo 4cm1 :Agente "+name+"Sobrepasó umbral CPU Go con :"+str(ultimo_valor), str(agentPath  ) +"CPU.png",str(agentPath  ) + "CPU.rrd")
	#	peirnt ("Envie correo ") 
	#	time.sleep(3600)
	
	
	#-----------------------------------------------------------------------------------------
		# 3 HDD de interfaz


		# 1 RAM de interfaz
#	if name=="linux" or name=="linuxmario":
	ramUsada = int(consultaSNMP(comunidad, ip, port, '1.3.6.1.2.1.25.2.3.1.6.36'))
	ramTotal = int(consultaSNMP(comunidad, ip, port, '1.3.6.1.2.1.25.2.3.1.5.36'))
	#else :
	#	ramUsada = int(consultaSNMP(comunidad, ip, port, '1.3.6.1.2.1.25.2.3.1.5.1'))
	#	ramTotal = int(consultaSNMP(comunidad, ip, port, '1.3.6.1.2.1.25.2.3.1.4.1'))
	valor = "N:" + str(ramUsada) + ':' + str(ramTotal)

	rrdtool.update(str(agentPath  ) + 'HDD.rrd', valor)
	rrdtool.dump(str(agentPath  ) + 'HDD.rrd' , str(agentPath  ) + 'HDD.xml' )


# 1 Grafica RAM de interfaz
	finalTime = int(rrdtool.last(str(agentPath  ) + "HDD.rrd"))
	initialTime = finalTime - 3600

	ret = rrdtool.graphv(
			str(agentPath  ) + "HDD.png",
			"--start", str(initialTime),
			"--vertical-label=Carga HDD",
			"--title=USO DE HDD - LINEA DE BASE",
			"--color", "ARROW#009900",
			'--vertical-label', "Uso de RAM (%)",
			'--lower-limit', '0',
			'--upper-limit', '100',
			"DEF:usada=" + str(agentPath  ) + "HDD.rrd:HDDusado:AVERAGE",
			"DEF:total=" + str(agentPath  ) + "HDD.rrd:HDDtotal:AVERAGE",
			
			"CDEF:porciento=usada,100,*,total,/",
			
			"VDEF:cargaSTDEV=usada,STDEV",

			"GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
			
			"AREA:porciento#00FF00:RAM Storage",
			'VDEF:ultimo=porciento,LAST',
			#'VDEF:ultimo2=carga,LAST',

			"VDEF:RAMlast=porciento,LAST",
			"VDEF:RAMmin=porciento,MINIMUM",
			"VDEF:RAMavg=porciento,AVERAGE",
			"VDEF:RAMmax=porciento,MAXIMUM",
			"VDEF:RAMmax2=porciento,STDEV",
			"CDEF:aux=porciento,5,+",
			"CDEF:aux2=porciento,2,+",
			"VDEF:RAMavg2=aux,AVERAGE",
			"VDEF:RAMavg3=aux2,AVERAGE",



			"HRULE:RAMavg2#BB0000:Umbral Go",
			"HRULE:RAMavg3#00BB00:Umbral Set",
			"HRULE:RAMavg#000000:Umbral Ready",

			"CDEF:umbral25=porciento,RAMavg2,LT,0,porciento,IF",
			"AREA:umbral25#FF9F00:Tráfico de carga mayor que umbral 3",
			
			#'CDEF:abc=porciento,RAMavg,100,LIMIT',
			"PRINT:RAMlast:%12.0lf%s",
			"PRINT:RAMavg2:%12.0lf%s ",
			

			"COMMENT:        Last              Now             Min                 Avg               Max//n",
			"GPRINT:RAMlast:%12.0lf%s",
			"GPRINT:RAMmin:%10.0lf%s",
			"GPRINT:RAMavg:%13.0lf%s",
			"GPRINT:RAMmax:%13.0lf%s",
			
	)
	
	#ultimo_valor= float(ret['print[0]'])
	#limite= float(ret['print[1]'])

	#print (ultimo_valor )

	#valores= ultimo_valor.split(" ")
	#lim=limite.split(" ")
	#print (name+"HDD valor" +str(ultimo_valor) + "limite "+ str(limite))
	#if float(ultimo_valor)>float(limite):
	#	sendAlertEmail("Agente "+name+"Sobrepasó umbral HDD Go con :"+str(ultimo_valor), str(agentPath  ) +"HDD.png",str(agentPath  ) + "HDD.rrd")
	


