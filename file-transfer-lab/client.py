#! /usr/bin/env python3

'''
Client - send files to the server
'''

import socket, sys, re

sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive

switchesVarDefaults = (
            (('-s', '--server'), 'server', "127.0.0.1:50001"),
            (('-d', '--debug'), "debug", False), # boolean (set if present)
            (('-?', '--usage'), "usage", False), # boolean (set if present)
            )

progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]
if usage:
            params.usage()
try:
        serverHost, serverPort = re.split(":", server)
        serverPort = int(serverPort)
except:
        print("Can't parse server:port from '%s'" % server)
        sys.exit(1)




addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)
#connection begins
s = socket.socket(addrFamily, socktype)

if s is None:
        print('could not open socket')
        sys.exit(1)

#if we connect successfully
s.connect(addrPort)
name = input("What is the file name?")

from framedSock import framedSend, framedReceive

#framedSend reads bytes from the file and sends them through a socket
#the server will receive and get the file
framedSend(s, name)
