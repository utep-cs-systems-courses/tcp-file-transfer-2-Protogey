def framedSend(sock, name):
    f = open(name, 'rb')
    l = f.read(1024)
    while(l):
        sock.send(l)
        l = f.read(1024)
    f.close()

def framedReceive(sock):
    with open('received_file', 'wb') as f:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            f.write(data)
    f.close()
