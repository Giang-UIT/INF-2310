from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
import rsa
from socket import *


class common(): 
    def __init__(self, end: str, portNumber: int, testMode: bool):
        self.end = end
        self.portNumber = portNumber
        
    def sending(self, message: any, socket: socket, portNumber: int): 
        
        if type(message) != bytes:
            message = message.encode()

        socket.sendto(message, ('127.0.0.1', portNumber))

        
    def receiving(self,socket:socket): 
        
        message, serverAddr = socket.recvfrom(4096)
        
        if message != None or serverAddr != None:
            
            return message, serverAddr
        
        return None

        
        
        
    
         
   
    