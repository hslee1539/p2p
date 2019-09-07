import socket
import threading
import random

import p2p

class Peer:
    """"""
    ip : str
    controlPort : int
    connectionPorts : list
    service : str
    peerList : list
    maxConnection : int
    serverThreads : list
    clientThreads : list
    serverState : list

    running : bool

    controlSocket : socket.socket
    controlThread : threading.Thread


    def __init__(self, service : str, controlPort : int, connectionPorts : list, peerList = []):
        self.peerList = peerList
        self.service = service
        self.controlPort = controlPort
        self.connectionPorts = connectionPorts
        self.maxConnection = len(connectionPorts)
        self.ip = socket.gethostbyname(socket.getfqdn())
        self.serverState = [False] * self.maxConnection
    
    def start(self):
        """"""
        self.running = True
        self.controlThread = threading.Thread(target=self._controlServer)
        self.controlThread.start()

        self.serverThreads = list(self._socketThreadGenerator(self._client))
        self.clientThreads = list(self._socketThreadGenerator(self._client))
        
        for serverThread in self.serverThreads:
            serverThread.start()
        for clientThread in self.clientThreads:
            clientThread.start()

        
    def _socketThreadGenerator(self, target : function):
        for index in range(self.maxConnection):
            yield threading.Thread(target=target, args=(index,))

    def _findSleepServerIndex(self):
        for i in range(self.maxConnection):
            if(self.serverState[i] == False):
                return i
        return self.maxConnection

    def _controlServer(self):
        """컨트롤 서버가 연결 유지가 가능한 포트를 클라이언트에 알려주도록 운영합니다."""
        with socket.socket() as sock:
            sock.bind((self.ip, self.controlPort))
            sock.settimeout(1)
            sock.listen()
            while(self.running):
                try:
                    clientSocket, address = sock.accept()
                except socket.timeout:
                    continue

                clientSocket : socket.socket
                
                try:
                    clientSocket.sendall(self.service.encode())
                    retval = clientSocket.recv(1024)
                    if (self.service == retval.decode()):
                        clientSocket.sendall(str(self.connectionPorts[self._findSleepServerIndex()]).encode())
                except socket.timeout:
                    pass
                finally:
                    clientSocket.close()

    def _server(self, index : int):
        """"""
        with socket.socket() as sock:
            sock.bind((self.ip, self.connectionPorts[index]))
            sock.settimeout(1)
            sock.listen()
            while(self.running):
                try:
                    self.serverState[index] = False
                    clientSocket, address = sock.accept()
                except socket.timeout:
                    continue
                clientSocket : socket.socket
                self.serverState[index] = True

                try:
                    clientSocket.sendall(self.service.encode())
                    retval = clientSocket.recv()
                    if (self.service == retval.decode()):

                except socket.timeout:
                    pass
                
                finally:
                    clientSocket.close()
    
    def _serverConnect(self):
        while (self.running):
            
                    
                

    def _client(self, index : int):
        """"""