#! /usr/bin/env python3

'''
Server - receive files from the client
'''

import sys
sys.path.append("../lib")       # for params

import re, socket, params, os

switchesVarDefaults = (
        (('-l', '--listenPort') ,'listenPort', 50001),
        (('-d', '--debug'), "debug", False), # boolean (set if present)
        (('-?', '--usage'), "usage", False), # boolean (set if present)
        )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)
#connection
while True:
    #accept
    sock, addr = lsock.accept()
    from framedSock import framedSend, framedReceive

    #implemented like the demo code, use framedSend
    if not os.fork():
        print("new child process handling connection from", addr)
        while True:
            framedReceive(sock)
            
