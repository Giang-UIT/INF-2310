from Crypto.Cipher import AES
from socket import *

class test(): 
    def __init__(self, end: str, portNumber: int):
        self.end = end
        self.portNumber = portNumber
        
        
    
    def sending(self, message: str, socket: socket, portNumber: int): 

        print(f"the {self.end} is sending message")
        socket.sendto(message.encode(), ('', portNumber))
        
        
        
    def receiving(self,socket:socket): 
        message, serverAddr = socket.recvfrom(2048)  
        print(f"the {self.end} received message: {message.decode()}")
        if message != None or serverAddr != None:
            
            return message, serverAddr
        

        return None
        
        
        
        
    
         
   
    