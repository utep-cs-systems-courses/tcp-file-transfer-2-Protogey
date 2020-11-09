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

class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
        self.fsock = EncapFramedSock(sockAddr)
    def run(self):
        lock = Lock()
        #here our receiving takes place, ask for the name youd like for the file
        #place received data into the given file name
        print("new thread handling connection from", self.addr)

        lock.acquire()
        try:
            name = input("What name would you like for the received file?")
            if path.exists(name):
                print("That file already exists..!")
                sys.exit(1)
                self.fsock.receive(name, debug)
            print("done receiving..!")
        finally:
            lock.release()

while True:
    sockAddr = lsock.accept()
    server = Server(sockAddr)
    server.start()
