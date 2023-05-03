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

defaultPort = 5050 #TODO: Set this to your preferred port 

 
 

def GetFreePort(minPort: int = 1024, maxPort: int = 65535): 

    for i in range(minPort, maxPort): 

        print("Testing port",i) 

        with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as potentialPort: 

            try: 

                potentialPort.bind(('localhost', i)) 

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

    with tcpSocket: 

        serverData = GetServerData() 

        print(f"Connected by {socketAddress}") 

 
 

        while True: 

            data = tcpSocket.recv(64).decode('utf-8') 

            if not data: 

                break 

 
 

            #send message to client 

            tcpSocket.sendall(bytes([0, 1, 2], 'utf-8')) 

    #pass; #TODO: Implement TCP Code, use GetServerData to query the database. 

 
 
 

def CreateTCPSocket() -> socket.socket: 

    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    #tcpPort = defaultPort 

    tcpPort = GetFreePort() 

    print("TCP Port:",tcpPort) 

    tcpSocket.bind(('localhost', tcpPort)) 

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

 
 

 