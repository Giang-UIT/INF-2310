from Crypto.Cipher import AES
from socket import *

class test(): 
    def __init__(self, end: str, portNumber: int):
        self.end = end
        self.portNumber = portNumber
        
        
    
    def sending(self, message: str, socket: socket, portNumber: int): 

        print(f"the {self.end} is sending message")
        socket.sendto(message.encode(), ('127.0.0.1', portNumber))
        
        
        
    def receiving(self,socket:socket): 
        print(f"the socket variable is: {socket} socket belongs to {self.end}")
        
        message, serverAddr = socket.recvfrom(2048)
          
        print(f"the {self.end} received message: {message.decode()}")
        if message != None or serverAddr != None:
            
            return message, serverAddr
        

        return None
        
        
        
        
    
         
   
    