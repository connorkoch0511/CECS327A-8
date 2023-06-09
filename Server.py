import socket 
import ipaddress 
import threading 
import time 
import contextlib 
import errno 
from dataclasses import dataclass 
import random 
import sys 

maxPacketSize = 1024 
defaultPort = 5050 #Set this to your preferred port 

def GetFreePort(minPort: int = 1024, maxPort: int = 65535): 
    for i in range(minPort, maxPort): 
        print("Testing port",i) 

        with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as potentialPort: 
            try: 
                potentialPort.bind(('10.182.0.2', i)) 
                potentialPort.close() 
                print("Server listening on port",i) 

                return i 
            except socket.error as e: 
                if e.errno == errno.EADDRINUSE: 
                    print("Port",i,"already in use. Checking next...") 
                else: 
                    print("An exotic error occurred:",e)

def GetServerData() -> list: 
    import MongoDBConnection as mongo 
    return mongo.QueryDatabase() 

def ListenOnTCP(tcpSocket: socket.socket, socketAddress): 
    message = tcpSocket.recv(64).decode()

    if message: 
        serverData = GetServerData() 

        print(f'Average time for Road A is {serverData[0]}')
        print(f'Average time for Road B is {serverData[1]}')
        print(f'Average time for Road C is {serverData[2]}')

        fastestHighway = min(serverData)
        letter = "A"

        if serverData[0] == fastestHighway:
            letter = "A"
        elif serverData[1] == fastestHighway:
            letter = "B"
        elif serverData[2] == fastestHighway:
            letter = "C"

        #send message to client 
        tcpSocket.sendall(bytes(letter, 'utf-8'))

def CreateTCPSocket() -> socket.socket: 

    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    #tcpPort = defaultPort 
    tcpPort = GetFreePort() 
    print("TCP Port:",tcpPort) 
    tcpSocket.bind(('10.182.0.2', tcpPort)) 
    return tcpSocket 

def LaunchTCPThreads(): 
    tcpSocket = CreateTCPSocket() 
    tcpSocket.listen(5) 

    while True: 
        connectionSocket, connectionAddress = tcpSocket.accept() 
        connectionThread = threading.Thread(target=ListenOnTCP, args=[connectionSocket, connectionAddress]) 
        connectionThread.start() 

if __name__ == "__main__": 
    tcpThread = threading.Thread(target=LaunchTCPThreads) 
    tcpThread.start() 

    while tcpThread.is_alive(): 
        time.sleep(1) 
    print("Ending program by exit signal...") 

 
 

 