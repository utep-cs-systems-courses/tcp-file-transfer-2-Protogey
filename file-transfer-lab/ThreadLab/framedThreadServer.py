#! /usr/bin/env python3

'''
Server - receive files from the clients
'''

import sys
sys.path.append("../lib")       # for params
import re, socket, params, os
from os import path

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

from threading import Thread;
from threading import Lock;
from encapFramedSock import EncapFramedSock
global fileSet, lock
lock = Lock()
fileSet = set()

class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
        self.fsock = EncapFramedSock(sockAddr)
    def run(self):
        #here our receiving takes place, ask for the name youd like for the file
        #place received data into the given file name
        print("new thread handling connection from", self.addr)
        lock.acquire()
        try:
            name = self.fsock.receiveName(debug)
            
            if path.exists(name):
                print("That file already exists..!")
                sys.exit(1)
            #if the file already is being transferred
            if name in fileSet:
                print("That file is already being transferred!")
                lock.release()
                sys.exit(1)
            fileSet.add(name)
            lock.release()
            self.fsock.receive(name, debug)
            print("done receiving..!")
            fileSet.remove(name)
        finally:
            print("Transfer complete")

while True:
    sockAddr = lsock.accept()
    server = Server(sockAddr)
    server.start()
