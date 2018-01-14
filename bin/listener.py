#!/usr/bin/env python

# Update for your bin directory
KP = "/home/jayson/bin/kp.py"

import datetime, os, socket, sys, thread
from subprocess import call
from thread import start_new_thread

usage_msg = "usage: {} valid_port_number".format(os.path.basename(sys.argv[0]))

try:
    port_val = int(sys.argv[1])
    if len(sys.argv) < 2 or port_val < 2**10 or port_val > 2**16-1:
        print usage_msg
        sys.exit(1)
except Exception as e:
    print usage_msg
    sys.exit(1)
 
HOST = ''		# Symbolic name meaning all available interfaces
PORT = port_val		# A non-privileged port

response_time = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S %Z')
# Note we are allowing *, assume you have things properly locked down
RESPONSE = """
HTTP/1.1 200 OK
Date: {}
Server: Custom
Last-Modified: {}
Content-Length: 8
Content-Type: text/html
Access-Control-Allow-Origin: *
Connection: Closed

Farewell
""".format(response_time, response_time)
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
 
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Socket bind failed. Error: ' + str(msg[0]) + ' Message: ' + msg[1]
    sys.exit()
     
s.listen(5)		# listen(backlog) - max number of queued connections
 
def client_thread(conn):
    first_post = True

    while True:
        data = conn.recv(1024).rstrip()
        has_content = True
        if "Content-Length: 0" in data: has_content = False
        data = data.split("\n")[-1]
        if not data or not(has_content):
            conn.send(RESPONSE)
            conn.close()
            break
        if not("Content" in data) or not("Accept-Language" in data):
            res = call([KP, data])
            if res == 0 or (res !=0 and not(first_post)):
                conn.send(RESPONSE)
                conn.close()
                break

        first_post = False
     
    conn.close()
 
while 1:
    conn, addr = s.accept()
    start_new_thread(client_thread ,(conn,))
 
s.close()
