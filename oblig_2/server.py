#! flask/bin/python3
from socket import *
from Crypto.Cipher import *
from Common import common

"""
serverName = "hostname"
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
"""

#enc_list = ["AES-256", "AES-196", "AES-128"]

#Child class that inherits from parent class
class server(common): 
    def __init__(self, end, portNumber):
        super().__init__(end, portNumber)
        self.portNumber = portNumber #server's port number
        self.socket = socket(AF_INET, SOCK_DGRAM) #Creating a socket for the server. Connection type is UDP, and the IP protocol is IPv4.
        self.socket.bind(('127.0.0.1',self.portNumber)) #Binding the socket to the port number of the server.
    
    def listening(self): 
        #Listening for incoming packets from the client. If a packet is received, the server will send an acknowledgment message back to the client.
        
        while True:
            packet = self.receiving() 
            print(f"Packet's content: {packet}")
            
            if packet != None:
                self.sending(packet)
            
            
    def sending(self, packet):
        
        
        return super().sending(packet[0], self.socket,packet[1][1]) #Sending the message to the port number of the client that sent the packet to the server.
    
    def receiving(self): #Receiving a packet from the client. If a packet is received, the server will return the packet
    
        #unpacking the package
        Packet =  super().receiving(self.socket)
        addr = Packet[1]
        Packet = Packet[0].decode()
        
        #if "e" flag is discovered, returns an ACK msg. 
        if Packet[0][0][0] == "e":     
            newPacket = ("eAck", addr)
                    
        else: #for other flags
            pass
        
        return newPacket
          
        
        

if __name__ == "__main__": 
    
    serverProgram = server("server", 12000)
    serverProgram.listening()