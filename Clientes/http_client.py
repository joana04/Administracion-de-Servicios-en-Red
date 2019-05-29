#!/usr/bin/env python
import http.client
from datetime import datetime

import sys
def check_webserver(address, port, resource):
    #create connection
    if not resource.startswith('/'):
        resource = '/' + resource
    try:
        time1=datetime.now()
        for i in range(1,10):
            conn = http.client.HTTPConnection(address, port)
            #print('HTTP connection created successfully')
            #make    request
            req = conn.request('GET', resource)
            #print('request for %s successful' % resource)
            # get response
            response = conn.getresponse()
        #print('response status: %s' % response.status)
    except sock.error as e:
        #print ("HTTP connection failed: %s' % e")
        return False
    finally:
        conn.close()
        #print ('HTTP connection closed successfully')
        time2=datetime.now()
        #print (time2-time1)
        if response.status in [200, 301]:
            return time2-time1
        else:
            return False

#check_webserver("localhost", 80, "index.html")