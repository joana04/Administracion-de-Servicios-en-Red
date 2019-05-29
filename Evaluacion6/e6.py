# coding=utf-8
from ftplib import FTP                                                                      
from datetime import time, datetime
import sys, time, os, errno
from notify import sendAlertEmail

#import getpass
#import sys
#import telnetlib

#python ftp_client.py localhost 21 bob 12345

lbPath = os.getcwd() + "/sc/"

def download(ip, user, password,filename): 
    lbPath = os.getcwd() + "/sc/"
    try:
        os.makedirs(os.path.dirname(lbPath))
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            print("Error de directorios: Linea Base.")
            raise 
    ftp = FTP(ip)                                                                               
    ftp.login(user,password)                                                                 
    files = ftp.nlst()                                                                           
    sc=open(lbPath+'sc'+ip+filename, 'wb')
    ftp.retrbinary('RETR ' + 'startup-config', sc.write)                                                                      
    sc.close() 
    ftp.quit()  

def upload(ip,user,password, filename, fndest, callback=None):
    ftp = FTP(ip)                                                                               
    ftp.login(user,password)                                                                 
    files = ftp.nlst() 

    with open(lbPath+filename, "rb") as f:
        ftp.storbinary("STOR " + fndest, f, callback=callback)                                               

    ftp.quit()
                                                                 

def ftp_client(ip, usuario, password):

    salida=""
    ftp = FTP(ip)                                                                               
    ftp.login(usuario,password)                                                                 
    files = ftp.nlst()    
    #download(ftp,ip) 
    #upload(ftp, 'hola', None)
    

#ftp_client("192.168.232.1", "rcp", "rcp")

def comparar(ip):
    with open(lbPath+"sc"+ip+"original") as a:
    #startup-confid192.168.232.1    "sc"+ip+"original"
        contentA = set(a)
    with open(lbPath+"sc"+ip+"new") as b:
    #startup-confid192.168.232.12    "sc"+ip+"new"
        contentB = set(b)
    res=contentA - contentB
    print (str(res))
    #print (res)
    if  res == set():
        print ("Son iguales")
    else:
        print("Son diferentes")
        print(res)
        #Enviar alerta 
       #sendAlertEmail("Diferencia en el router de ip :"+ ip+" "+str(res), lbPath+"sc"+ip+"original",lbPath+"sc"+ip+"original")
    #   print ("Envie correo ") 


"""

def telnet(ip, user, password):

    HOST = user
    #user = raw_input("Enter your remote account: ")
    #password = getpass.getpass()

    tn = telnetlib.Telnet(HOST)

    tn.read_until("login: ")
    tn.write(user + "\n")
    if password:
        tn.read_until("Password: ")
        tn.write(password + "\n")

    tn.write("ls\n")
    tn.write("exit\n")

    print tn.read_all()

"""

#comparar("192.168.232.1")