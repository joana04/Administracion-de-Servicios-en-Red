# coding=utf-8
from ftplib import FTP                                                                      
from datetime import time, datetime
import sys
#python ftp_client.py localhost 21 bob 12345

def download(ftp, files, j):                                                                            
    print ("Descargando=>"+files[j] )     
    fhandle = open(files[j], 'wb')
    ftp.retrbinary('RETR ' + files[j], fhandle.write)                                       
    fhandle.close()
    return ("Descargando =>"+ files[j])                                                   


#ip          = sys.argv[1]                                                                   
#puerto      = sys.argv[2]                                                                   
#usuario     = sys.argv[3]                                                                   
#password    = sys.argv[4]                                                                   

def ftp_client(ip, usuario, password):
    salida=""
    ftp = FTP(ip)                                                                               
    ftp.login(usuario,password)                                                                 
    files = ftp.nlst()                                                                          
    #for i,v in enumerate(files,1):                                                              
     #   print (i+"->"+v)
    #print("")
    time1 = datetime.now()
    i=0
    for x in range(1, 10):
        if i==0:                                                                                    
            for j in range(len(files)):                                                             
                salida=download(ftp, files, j)                                                                         
        if i>0 and i<=len(files):                                               
            download(i-1) 
    time2 = datetime.now()
    time3 = time2 - time1
    #print ("Tiempo de operación: " +str(time3)+ "segundos.") 
    return str(time3)+"||"+"Archivos descargados"+"||"

#ftp_client("localhost", "usuario1", "usuario1")


