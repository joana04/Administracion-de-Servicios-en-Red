import dns.resolver
from time import time

# Instalar el modulo sudo pip install dnspython
# Un ejemplo para correr el script es: 
#   python clientDNS.py -a 1.1.1.1 -d 172.217.15.14 -n 5 -p 53
#   python clientDNS.py -a 1.1.1.1 -d google.com -n 5

def validate_ip(s):
	a = s.split('.')
	if len(a) != 4:
		return False
	for x in a:
		if not x.isdigit():
			return False
		i = int(x)
		if i < 0 or i > 255:
			return False
	return True

def dnsServer(address,port,domain,requests):
	myResolver = dns.resolver.Resolver()
	myResolver.port = int(port)
	myResolver.nameservers = [str(address)]
	try:
		if validate_ip(str(domain)):
			start_time = time()
			for i in range(0,int(requests)):
				req = '.'.join(reversed(domain.split("."))) + ".in-addr.arpa"
				myAnswers = myResolver.query(str(req), "PTR")
				#for rdata in myAnswers:
						#print("Ip: " + str(domain) + "\nDomain: " + str(rdata))
			return time() - start_time
		else:
			start_time = time()
			for i in range(0,int(requests)):
				myAnswers = myResolver.query(str(domain), "A")
				#for rdata in myAnswers:
						#print("Domain: " + str(domain) + "\nIp: " + str(rdata))
			return time() - start_time
					
	except Exception as e: 
		print(e)
		return -1

# if __name__ == '__main__':
#     from optparse import OptionParser
#     parser = OptionParser()
#     parser.add_option("-a","--address", dest="address", default='localhost',
#                     help="ADDRESS for DNS server")
#     parser.add_option("-p", "--port",dest="port", type="int", default=53,
#                     help="PORT for DNS server")
#     parser.add_option("-d", "--domain", dest="domain", default='localhost',
#                     help="Domain or IP to consult")
#     parser.add_option("-n", "--number", dest="requests", default=1,
#                     help="Number of requestsbbb")
#     (options, args) = parser.parse_args()
#     dnsServer(str(options.address), options.port, options.domain, options.requests)