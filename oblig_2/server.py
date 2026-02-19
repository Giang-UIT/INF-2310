#! flask/bin/python3
from socket import *
from Crypto.Cipher import AES
from running import test

"""
serverName = "hostname"
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
"""

class server(test): 
    def __init__(self, end, portNumber):
        super().__init__(end, portNumber)
        self.portNumber = portNumber
        self.serverName = 'host name'
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(('',self.portNumber))
        self.hostName = end + " program"
    
    def listening(self): 
        
        while True:
            
            message = self.receiving()
            if type(message) == str and message != None: 
                print(message)
                self.sending()
            
            
    def sending(self):
        msgAck = "Message from server"
        return super().sending(msgAck)
    
    def receiving(self):
        return super().receiving(self.socket) 
        

if __name__ == "__main__": 
    serverProgram = server("server", 12000)
    serverProgram.listening()