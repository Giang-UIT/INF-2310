from Crypto.Cipher import AES
from socket import *


class common(): 
    def __init__(self, end: str, portNumber: int):
        self.end = end
        self.portNumber = portNumber
        
    def sending(self, message: any, socket: socket, portNumber: int): 
        #print(f"the {self.end} is sending message: {message}")
        if type(message) != bytes:
            message = message.encode()

        socket.sendto(message, ('127.0.0.1', portNumber))

        
    def receiving(self,socket:socket): 
        
        message, serverAddr = socket.recvfrom(4096)
          
        #print(f"the {self.end} received message: {message.decode()}")
        if message != None or serverAddr != None:
            
            return message, serverAddr
        
        return None
        
        
        
        
    
         
   
    