import rrdtool
import  time
from pysnmp.hlapi import *
from Hilo import Hilo
from Graficar import crearBases
from Herramientas import estatus
from Herramientas import getInterfaces
from Herramientas import getSI
from Herramientas import getsnmp
from LineaBase import crearBasesLb
from MinimoCuadrado import creaeBasesMC
from Prediccion import crearBasesP


class MonitorGeneral:

    
    def verDisp(self, ban):
        cadena=""
        entra=1
        ip=""
        grupo=""
        pto=""
        v=1
        nd=0
        disp=open("Dispositivos.txt","a")
        disp.close()
        disp=open("Dispositivos.txt", "r")  
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
            pto=cadena[4]
            """ ag=(cadena[0],
                    cadena[2],
                    cadena[1],
                    int(pto),
                    cadena[3],
                    cadena[5],
                    int(cadena[6])
                    )
            t = Hilo(ag)
            t.start()"""
            print("Dispositivo---> "+ cadena[0])
            if estatus(cadena[2],cadena[3]) ==1:
                getInterfaces(ip,grupo,v)
                getSI(ip,grupo,v)
                if ban==0:   
                    ag=(cadena[0],
                            cadena[2],
                            cadena[1],
                            int(pto),
                            cadena[3],
                            cadena[5],
                            int(cadena[6])
                            )
                    #print ("-----------"+ str(ag[0]) )       
                    t = Hilo(ag)
                    t.start() 
                    print("Trabajando prediccion ")
                    ##print ("hilo aqui" + str(t.isAlive()))
            elif cadena[0]=="prueba":
                print("probando")
                getsnmp(ip,grupo,v, "1.3.6.1.2.1.1", cadena[4])
            else:
                break

        disp.close()



    def agregarDisp(self):
        
        print("\n\t Agregar dispositivo")
        print("Introduzca el Hostname")
        hostname=str(input())
        print("Introduzca el número de versión SNMP (1,2,3), en caso de no saberlo introduzca 0")
        ver=str(input())
        print ("Introduzca la dirección IP ")
        ip=str(input())
        print ("Introduzca la cominudad")
        com=str(input())
        print ("Introduzca el puerto")
        pto=str(input())
        print ("Introduzca el umbral para Minimos Cuadrados")
        mc=str(input())
        print(hostname+"||"+ver+"||"+ip+"||"+com+"||"+"\n")
        disp=open("Dispositivos.txt", "a")
        tiempo_actual = int(time.time())    
        disp.write(hostname+"||"+ver+"||"+ip+"||"+com+"||"+pto+"||"+str(tiempo_actual)+"||"+str(mc)+"||\n")
        disp.close()
        if estatus(ip,com)== 1:
            print ("Dispositivo trabajando")
            crearBases( hostname )
            time.sleep(1)
            crearBasesLb(com, ip, pto,hostname)
            time.sleep(1)
            creaeBasesMC(com, ip, pto,hostname)
            time.sleep(1)
            crearBasesP(com, ip, pto,hostname)
            time.sleep(1)
            ag=(hostname,
                    ip,
                    ver,
                    int(pto),
                    com,
                    tiempo_actual,
                    int(mc))
            t = Hilo(ag)
            t.start()
            print("lanzo hilo con prediccion")
        else :
          """  print ("Dispositivo trabajando")
            crearBases( hostname )
            time.sleep(1)
            crearBasesLb(com, ip, pto,hostname)
            time.sleep(1)
            creaeBasesMC(com, ip, pto,hostname)
            time.sleep(1)
            ag=(hostname,
                    ip,
                    ver,
                    int(pto),
                    com,
                    tiempo_actual,
                    int(mc))
            t = Hilo(ag)
            t.start()
            print("lanzo hilo")"""
            #print("Creoq ue algo slio mal ")


    def eliminarDisp(self):
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
                nuevos=nuevos+linea
        print(nuevos)
        disp.close()
        nuevo=open("Dispositivos.txt","w")
        nuevo.write(nuevos)
        nuevo.close()


    def consulta( self ):
        print("Introduzca el Hostname que desea monitorear")
        hostname=str(input())   
        disp= open("Dispositivos.txt","r")
        for linea in disp:
            cadena=linea.split("||")
            print (cadena[0] + hostname)
            ip=cadena[2] 
            grupo=cadena[3]
            v=int(cadena[1])
            encontrado = False
            if cadena[0]==hostname:
                print("\t\tInformacion del agente  ")
                print( "Nombre del host: " + cadena[0] )
                print( "IP del host: " + ip )
                print( "Version: " + cadena[1] )
                print( "Numero de Interfaces de Red: " + getsnmp(ip,grupo,v, "1.3.6.1.2.1.2.1.0", cadena[4] ))
                print( "Tiempo actividad desde ult reset: " + getsnmp(ip,grupo,v,'1.3.6.1.2.1.1.3.0', cadena[4]) )
                print( "Ubicacion fisica: " + getsnmp(ip,grupo,v,'1.3.6.1.2.1.1.6.0', cadena[4]) )
                print( "Contacto admin: " + getsnmp(ip,grupo,v,'1.3.6.1.2.1.1.4.0',cadena[4]) )
                encontrado = True
        return encontrado

    def minimosCuadrados(self):
        print("  \n\tEJECUCIÓN DE MINIMOS CUADRADOS\n")
        print("Nombre del archivo rrd: ")
        nombreArchivo=str(input())
        print("Nombre de la variable rrd: ")
        variable=str(input())
        """print("Tiempo de inicio: ")
        inicio=str(input())
        print("Tiempo final: ")
        fin=str(input())"""
        print("Umbral: ")
        umbral=str(input())

        EjecutarMC(nombreArchivo, variable, 1, 1, umbral)

        


