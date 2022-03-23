import xmlrpc.client
import socket
import datetime

#Client socket to connect to server socket
ClientMultiSocket = socket.socket()
host = 'localhost'
port = 9000
print('Waiting for connection response')
try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))
res = ClientMultiSocket.recv(2048)
while True:
    #rpc
    with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy:
        Input = input('Give topic: ')
        if(Input == "break"):
            break
        Input2 = input('Give text: ')
        Input4 = input('Description: ')
        Input3 = datetime.datetime.now()
        #Print what's returned from rpc call
        print(proxy.text(Input, Input2, Input4, str(Input3)))
ClientMultiSocket.close()
