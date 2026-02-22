from Crypto.Cipher import AES
from socket import *
from running import test


class client(test): 
    def __init__(self, end, portNumber):
        super().__init__(end, portNumber)
        self.portNumber = portNumber
        self.socket = socket(AF_INET, SOCK_DGRAM) #Creating a socket for the server. Connection type is UDP, and the IP protocol is IPv4.
        self.socket.bind(('127.0.0.1',self.portNumber)) #Binding the socket to the port number of the client.
    
    def sending(self):
        message = input("write message here: ")
        
        return super().sending(message,self.socket,12000) #Sending the message to the port number of the server.
    
    def receiving(self):
        #Receiving a packet from the server. If a packet is received, the client will print the message.

        message =  super().receiving(self.socket) 
        print(f"the client is receiving an incomming packet with the message being: {message[0].decode()}")
    
    def close(self):
        return self.socket.close()

if __name__ == "__main__": 
    clientProgram = client("client", 12001)
    clientProgram.sending()
    clientProgram.receiving()
    clientProgram.close()
    
    
    