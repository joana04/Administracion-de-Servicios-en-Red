import rrdtool, time, os, errno
from getSNMP import consultaSNMP, walkSNMP
from notify import sendAlertEmail
from notify import check_aberration

lbPathmc = os.getcwd() + "/rrd/prediccion/"
def crearBasesP(comunidad, ip, port, name):
	
	agentPath = lbPathmc + name + "/"
	try:
		os.makedirs(os.path.dirname(agentPath))
	except OSError as exc:
		if exc.errno != errno.EEXIST:
			print("Error de directorios: prediccion.")
			raise
	
	ret=rrdtool.create(agentPath + name + "netPred.rrd",
		'--start','N','--step','1',
		"DS:inoctets:COUNTER:600:U:U",
		"RRA:AVERAGE:0.5:1:1200",
		"RRA:HWPREDICT:1000:0.1:0.0035:10:3",
		"RRA:SEASONAL:10:0.1:2",
		"RRA:DEVSEASONAL:10:0.1:2",
		"RRA:DEVPREDICT:1000:4",
		"RRA:FAILURES:1000:3:5:4")

	if ret:
		print(rrdtool.error())


def EjecutarP( hilo, comunidad , ip , port , name  ):
	agentPath = lbPathmc  + name + "/"
	fname="netPred.rrd"


	consulta = int(consultaSNMP( comunidad , ip , port ,'1.3.6.1.2.1.2.2.1.10.1'))
	valor = "N:" + str(consulta)
	ret = rrdtool.update(str(agentPath + name+fname), valor)
	rrdtool.dump(str(agentPath +name+ fname),str(agentPath)+name +'netP.xml')

	
	title="Deteccion de comportamiento anomalo"


	ultimo=rrdtool.last(str(agentPath + name+fname))
	#cambia el valor de alfa
	rrdtool.tune(str(agentPath + name + fname),'--alpha','0.8')
	#rrdtool.tune(str(agentPath + name + fname),'--beta','0.1')
	#rrdtool.tune(str(agentPath + name + fname),'--gamma','0.1')

	ret = rrdtool.graphv(str(agentPath+name)+"prediccion.png",
						'--start', str(ultimo-100), '--end', str(ultimo+5), '--title=' + title,
						"--vertical-label=Bytes/s",
						'--slope-mode',
						"DEF:obs="       + str(agentPath + name + fname) + ":inoctets:AVERAGE",
						#"DEF:outoctets=" + str(agentPath + fname) + ":outoctets:AVERAGE",
						"DEF:pred="      + str(agentPath + name + fname) + ":inoctets:HWPREDICT",
						"DEF:dev="       + str(agentPath + name + fname) + ":inoctets:DEVPREDICT",
						"DEF:fail="      + str(agentPath + name + fname) + ":inoctets:FAILURES",

					 #"RRA:DEVSEASONAL:1d:0.1:2",
					 #"RRA:DEVPREDICT:5d:5",
					 #"RRA:FAILURES:1d:7:9:5""
						"CDEF:scaledobs=obs,8,*",
						"CDEF:upper=pred,dev,2,*,+",
						"CDEF:lower=pred,dev,2,*,-",
						"CDEF:scaledupper=upper,8,*",
						"CDEF:scaledlower=lower,8,*",
						"CDEF:scaledpred=pred,8,*",
						"TICK:fail#FDD017:1.0:FFallas",
						"LINE3:scaledobs#00FF00:In traffic",
						"LINE1:scaledpred#FF00FF:Prediccion\\n",
						#"LINE1:outoctets#0000FF:Out traffic",
						"LINE1:scaledupper#ff0000:Upper Bound Average bits in\\n",
						"LINE1:scaledlower#0000FF:Lower Bound Average bits in",

						"VDEF:lastfail=fail,LAST",
						#"VDEF:max=fail,MAXIMUM",
                     	#"VDEF:min=fail,MINIMUM",
						"PRINT:lastfail: %c :strftime",
					 	"PRINT:lastfail:%6.2lf %S ",
					 	'PRINT:fail:MIN:%1.0lf',
				   		'PRINT:fail:MAX:%1.0lf',)

	#bandera=0
	time_falla=ret['print[0]']
	ultima_falla= ret['print[1]']
	fmin= ret['print[2]']
	fmax= ret['print[3]']
	
	
	#f = open(str(agentPath)+"log.txt","a")
	#print("Fallas "+ str(ultima_falla) +"----"+ str(time_falla))

	if float(ultima_falla)==1 :
		if hilo.ban==0: # inicio de falla bandera de 0 a 1 
			hilo.inicio=str(time_falla)
			hilo.ban=1
			print ("INICIO DE FALLA")
			if hilo.unaVez==0:
				sendAlertEmail("Agente : "+name +" Inicio aberración : "+str(hilo.inicio), str(agentPath)+"prediccion.png",str(agentPath+name+fname))
				hilo.unaVez=1
		elif hilo.ban==1:# aun no termina la falla y gardo el ultimo tiempo
			hilo.fin=str(time_falla)
			print ("CONTINUA"+ hilo.fin)
	elif float(ultima_falla)==0 and hilo.ban==1: #termina la falla bandera de 1 a 0
			hilo.ban=0

			f = open(str(lbPathmc)+"log.txt","a")
			f.write(str("\tFalla "+ name+"\n"))
			f.write("Inicio : "+str(hilo.inicio)+"\n")
			if hilo.fin=="":
				hilo.fin=str(time_falla)
				f.write("Fin: "+str(hilo.fin)+"\n")
			else :
				f.write("Fin: "+str(hilo.fin)+"\n")
			print ("FIN DE FALLA"+ hilo.fin)
			if hilo.unaVez==1:
				sendAlertEmail("Agente : "+name +" Fin aberración : "+str(hilo.fin), str(agentPath)+"prediccion.png",str(agentPath+name+fname))
				hilo.unaVez=2
			hilo.fin=""
			hilo.inicio=""
			f.close()
		


		#sendAlertEmail("Agente "+name+" sobrepasó umbral de minimos cuadrados"+str(ultimo_valor), str(agentPath + name)+"deteccion.png",str(agentPath + str(name)) + 'trend.rrd')
	#elif( float(ultimo_valor)==0):
	#	sendAlertEmail("Agente "+name+" sobrepasó umbral 0 de minimos cuadrados"+str(ultimo_valor), str(agentPath + name)+"deteccion.png",str(agentPath + str(name)) + 'trend.rrd')
	

	#time.sleep(1)



#crearBasesP("gr_4cm1", "192.168.1.95", "161", "lin")
#print ("listillo")

#while 1:
	#f = open(str(agentPath)+"log.txt","a")
#	EjecutarP( "gr_4cm1", "192.168.1.95", "161", "lin" )+
