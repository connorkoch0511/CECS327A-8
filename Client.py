import socket 

import ipaddress 

import threading 

import time 

import contextlib 

import errno 

 
 

maxPacketSize = 1024 

defaultPort = 5050 #Change this to your expected port 

serverIP = '10.182.0.2' #Change this to your instance IP 

print(socket.gethostbyname(socket.gethostname()))

 
 

tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

try: 

    tcpPort = int(input("Please enter the TCP port of the host...")) 

except: 

    tcpPort = 0 

if tcpPort == 0: 

    tcpPort = defaultPort 

tcpSocket.connect((serverIP, tcpPort)) 

 
 

clientMessage = "" 

while clientMessage != "exit": 

    clientMessage = input("Please type the message that you'd like to send (Or type \"exit\" to exit):\n>") 

 
 

    #Send the message to your server 

    tcpSocket.sendall(bytes(clientMessage, 'utf-8')) 

    #Receive a reply from the server for the best highway to take 

    m = tcpSocket.recv(64).decode('utf-8') 

    #Print the best highway to take 

    print('Server says best highway to take is ' + m) 

     

tcpSocket.close() 

 