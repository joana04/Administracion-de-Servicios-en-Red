import paramiko
import os
import time
from getSNMP import consultaSNMP, walkSNMP

#python3 clientSSH -a 192.168.122.1 -u esli -p morado 



def sshClient(host, username, password,petitiones,port, comunidad, snmpport):
	print("-------SSH------")
	datos=dict(hostname=host, port=port,username=username, password=password)
	ssh_client=paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	start_time = int (time.time())
	try:
		ssh_client.connect(**datos)
		for i in range(0, int(petitiones)):
			salida=ssh_client.exec_command('who')
			#if salida:
				#print (salida.read())
				#print("------ TODO COOL  ------\n")
				
			#else:
			#	print ("Down")
	except Exception as e:
		print (e)

	final_time=int(time.time())
	aux=str(salida[0]).split(";")
	print("Canales abiertos: "+ aux[1])

	#print("\n tiempo de actividad "+ str(float(final_time-start_time)))
	int_octets= int(consultaSNMP( comunidad , host , snmpport ,'1.3.6.1.2.1.2.2.1.10.1'))
	out_octets= int(consultaSNMP( comunidad , host, snmpport ,'1.3.6.1.2.1.2.2.1.16.1'))
	print("\n tiempo de actividad SSH"+ str(float(final_time-start_time))+"\n Octetos\n Entrada:"+ str(int_octets)+"\n Salida:"+str(out_octets) )

	return str(final_time)+"||"+str(int_octets)+"||"+str(out_octets)+"||"+aux[1]+"||"
	ssh_client.close()

"""if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-a","--hostssh", dest="hostssh", default='localhost')
    parser.add_option("-u", "--username", dest="username", default='esli')
    parser.add_option("-p", "--password",dest="password", default='morado')
    parser.add_option("-n", "--number", dest="petitiones", default=1)
    (options, args) = parser.parse_args()
sshClient(str(options.hostssh), str(options.username), options.password, options.petitiones, 22)
"""
