import rrdtool
import  time
from pysnmp.hlapi import *
from Herramientas import *
from e6 import *
from getSNMP import consultaSNMP, walkSNMP
from Hilo import Hilo
from LineaBase import crearBasesLb



class MonitorGeneral:

    def verDisp(self):
        print ("\n\tEvaluación de todos los dispositivos")
        disp=open("Dispositivos.txt", "r")
        for linea in disp:      
            cadena=linea.split("||")
            ip=cadena[0] 
            user=cadena[1]
            password=cadena[2]
            community=cadena[3]
            print("Dispositivo---> "+ cadena[0])
            download(ip, usr, pas, "new")
            comparar(ip)
        disp.close()

    def iniciar(self):
        print ("\n\tInicio Hilos")
        disp=open("Dispositivos.txt", "r")
        for linea in disp:      
            cadena=linea.split("||")
            ip=cadena[0] 
            user=cadena[1]
            password=cadena[2]
            community=cadena[3]
            time=cadena[4]
           """ ag=(ip,
                ip,
                "1",
                161,
                community,
                time)
            t = Hilo(ag)
            t.start()"""
        disp.close()

    def verUnDisp(self):
        print("\n\t Evaluacion de un dispositivo")
        print("Introduzca la ip del dispositivo")
        ip=str(input())   
        disp= open("Dispositivos.txt","r")
        for linea in disp:
            cadena=linea.split("||")
            aip=cadena[0] 
            user=cadena[1]
            password=cadena[2]
            community=cadena[3]
            if aip==ip:
                print("Evaluación de dispositivo: " + aip )
                download(aip, user, password, "new")
                comparar(aip)
            else:
                ("Dispositivo no encontrado")
        disp.close()


    def agregarDisp(self):
        print("\n\t Agregar dispositivo")
        print ("Introduzca la dirección IP ")
        ip=str(input())
        print ("Introduzca el usuario")
        usr=str(input())
        print ("Introduzca la contraseña")
        pas=str(input())
        print ("Introduzca la cominudad")
        com=str(input())
        tiempo_actual = int(time.time()) 
        disp=open("Dispositivos.txt", "a")
        disp.write(ip+"||"+usr+"||"+pas+"||"+com+"||"+ str(tiempo_actual) +"||\n")
        disp.close()
        print("Se agrego el dispositivo: "+ip+"||"+usr+"||"+pas+"||"+com+"||"+"\n")
        download(ip, usr, pas, "original")
        print("se decargo el archivo de configuración inicial ")
        inventario(ip, com)
        crearBasesLb(com, ip, 161,ip)
        ag=(ip,
            ip,
            "1",
            161,
            com,
            tiempo_actual)
        t = Hilo(ag)
        t.start()
        print("lanzo hilo con linea base")



    def enviarArchivo(self):
        print("\n\t Enviar archivo a un dispositivo")
        print("Introduzca la ip del dispositivo")
        ip=str(input())   
        print("Introduzca el nombre del archivo a enviar")
        fn=str(input())   
        print("Introduzca el nombre para almacenar en el router")
        fnd=str(input())   

        disp= open("Dispositivos.txt","r")
        for linea in disp:
            cadena=linea.split("||")
            aip=cadena[0] 
            user=cadena[1]
            password=cadena[2]
            community=cadena[3]
            if aip==ip:
                print("Enviando: " + aip )
                upload(ip,user,password, fn, fnd, callback=None)
            else:
                ("Dispositivo no encontrado")

        disp.close()

    

    def verInventario( self, ip, comunidad ):
        print ("\n\tInventario\n")
        disp= open("Inventario.txt","r")
        for linea in disp:
            print (linea)
        disp.close()

 


