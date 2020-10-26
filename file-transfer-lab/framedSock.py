#send a file
def framedSend(sock, name):
    #open file in read bytes
    f = open(name, 'rb')
    l = f.read(1024)#read 1024 bytes
    while(l):
        sock.send(l)
        l = f.read(1024)
    f.close()

#receive a file
def framedReceive(sock):
    with open('Received_file', 'wb') as f:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            f.write(data)
