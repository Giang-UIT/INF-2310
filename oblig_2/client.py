from Crypto.Cipher import AES
from socket import *
from running import test


class client(test): 
    def __init__(self, end, portNumber):
        super().__init__(end, portNumber)
        self.portNumber = portNumber
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.msg = "Hello from the other side."
        self.hostName = end + " program"
    
    def sending(self):
        message = input("write message here: ")
        
        return super().sending(message,self.socket)
    
    def receiving(self):
        message =  super().receiving(self.socket)
        print(message)
    
    def close(self):
        return self.socket.close()

if __name__ == "__main__": 
    clientProgram = client("client", 12000)
    clientProgram.sending()
    clientProgram.receiving()
    clientProgram.close()
    
    
    