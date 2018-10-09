import socket
import sys
import time
from payload import *
import pickle
import string

def create_server(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Socket Created")
    except socket.error as error:
        print("Failed to create socket. Error code:" + str(error[0]) + 'Message' + error[1])
        sys.exit()

    try:
        s.bind((host, port))
    except socket.error as error:
        print("Bind failed. Error Code :", error)
        sys.exit()

    print("Socket bind complete")

    return s

def create_client(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Socket Created")
    except socket.error as error:
        print("Failed to create socket. Error code:" + str(error[0]) + 'Message' + error[1])
        sys.exit()
    return s

def recv(s,port):    
    
    while(1):
        
        data, add = s.recvfrom(4096)
        packet = pickle.loads(data)
        send_confirm(s, packet, add)
    
    s.close()    

def send_confirm(s, header,port):
    
    ack = payload("ack", header.ack,header.seqNumber, header.destiny, header.font)
    orig = ack.font
    print(orig, port)
    ack = pickle.dumps(ack)
    s.sendto(ack, port)
    
def send(s,host_s, port, data, host_c):
    
    aux = time.time()

    seqNumber = 0
    ack = len(data.encode()) + seqNumber
    msg = payload(data,ack , seqNumber, host_c, host_s)
    msg = pickle.dumps(msg)

    try :
        s.sendto(msg, (host_s, port))
        print(host_s, port)

    except socket.error as error:
        print("Error Code :" + str(error[0]) + "Message" + error[1])
        sys.exit()

    while (time.time() - aux) < 4:  
        s.settimeout(100)  
        data, add = s.recvfrom(4096)
        packet = pickle.loads(data)
        print(data)