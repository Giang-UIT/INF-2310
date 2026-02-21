from Crypto.Cipher import AES
from socket import *

class test(): 
    def __init__(self, end: str, portNumber: int):
        self.end = end
        self.portNumber = portNumber
        
        
    
    def sending(self, message: str, socket: socket): 
        
        socket.sendto(message.encode(), (self.end, self.portNumber))
        
        print(f"the {self.end} is sending message")
            
        
        
    
    def receiving(self,socket:socket): 
        message, serverAddr = socket.recvfrom(2048)   
        
        return message.decode().upper()
        
        
        
    
         
   
    