import paramiko
import os

#python3 clientSSH -a 192.168.122.1 -u esli -p morado 



def sshClient(host, username, password,petitiones,port):
	datos=dict(hostname=host, port=port,username=username, password=password)
	ssh_client=paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_client.connect(**datos)
	entrada,salida,error=ssh_client.exec_command('ls -la')
	if salida:
		#print (salida.read())
		print("TODO COOL")
	else:
		print ("Error en la conexión")
	ssh_client.close()


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-a","--hostssh", dest="hostssh", default='localhost')
    parser.add_option("-u", "--username", dest="username", default='esli')
    parser.add_option("-p", "--password",dest="password", default='morado')
    parser.add_option("-n", "--number", dest="petitiones", default=1)
    (options, args) = parser.parse_args()
sshClient(str(options.hostssh), str(options.username), options.password, options.petitiones, 22)

