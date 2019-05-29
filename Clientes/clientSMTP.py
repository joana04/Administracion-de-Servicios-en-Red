import os
import socket
import smtplib
import time

def send_mail (from_host, usuario, ip, dominio, puerto, subject, text):
	to_host=usuario+"@"+ip
	tiempo_inicial=int (time.time())

	msg=("From: {0}\nTo: {2}\nSubject: {2}\n{3} ".format(from_host, to_host, subject, text).encode('utf-8'))
	server=smtplib.SMTP()
	server.connect(ip, dominio)
	try:
		server.sendmail(from_host, to_host,msg)
		tiempo_final=int(time.time())

		print("Tiempo de respuesta"+str(tiempo_final-tiempo_inicial))

	finally:
		server.quit()

	return

def star_snmp_sensor():
	from_host='@'.join([os.getenv("LOGNAME"), socket.gethostname()])
	usuario=input("Escriba el nombre de usuario destino:")
	ip=input("Escriba la direccion ip destino:")
	dominio=input("Escriba el dominio:")
	puerto=input("Escriba el puerto del dominio:")
	sbj="Probando el envio local en python"
	txt="Si esti aparece, esto eta bien"
	send_mail(from_host, usuario, ip, dominio, puerto, sbj, txt)
	print ("Checate tu bandeja de entrada")

def get_Attachments(msg):
	for part in msg.walk():
		if part.get_contect_maintype()=='multipart':
			continue
		if part.get('Contect-Disposition') is None:
			continue
		file_name=part.get_filename()

		if bool(file_name):
			file_path=os.path.join(attachment_dir, file_name)
			with open(file_path, 'wb') as f:
				f.write(part.get_payload(decode=True))

def search(key, value, conn):
	res,d=conn.search(None, key, '"{}"'.format(value))
	return d

def gte_email(result_bytes):
	msgs=[]
	for num in result_bytes[0].split():
		typ, d = conn.fetch(num, '(RFC822)')
		msgs.append(d)
		return msgs

#con=auth(user, pasword, imap_url)
#con.select('INBOX')

#result, data = con.fetch(b'10', 'RFC822')
#raw=email.message_from_bytes(data[0][1])
#get_attachments(raw)

star_snmp_sensor()
