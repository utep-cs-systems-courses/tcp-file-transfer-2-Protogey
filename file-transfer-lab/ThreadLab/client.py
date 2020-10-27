#! /usr/bin/env python3

# file transfer client, updated to threads
import socket, sys, re

sys.path.append("../lib")       # for params
import params

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

#receive the file from the framed sock
#name = input("What do you wanna name the file?")
fsock.receive(debug)
print("done receiving")
fsock.close()
