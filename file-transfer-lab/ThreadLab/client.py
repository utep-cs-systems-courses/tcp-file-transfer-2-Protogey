#! /usr/bin/env python3

'''
Client - transfer a file from a client to the server
'''

# file transfer client, updated to threads
import socket, sys, re, os

sys.path.append("../lib")       # for params
import params

#used to transfer files to the server
from encapFramedSock import EncapFramedSock

switchesVarDefaults = (
            (('-s', '--server'), 'server', "127.0.0.1:50001"),
            (('-d', '--debug'), "debug", False), # boolean (set if present)
            (('-?', '--usage'), "usage", False), # boolean (set if present)
            )

progname = "client"
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
sock = socket.socket(addrFamily, socktype)

if sock is None:
        print('could not open socket')
        sys.exit(1)

#if we connect successfully 
sock.connect(addrPort)
#create encapFramedSock using our socket and port
fsock = EncapFramedSock((sock, addrPort))

#get the file name, attached should be the extension(.txt, .pdf, etc...)
name = input("What file do you want to send?")
#check the file size is not 0, if it is handle error by exit
if os.path.getsize(name) == 0:
            print("file size 0")
            sys.exit(1)
#send to the server, print and close when done
fsock.send(name, debug)
print("done sending..!")
fsock.close()
