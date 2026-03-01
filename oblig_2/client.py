from Crypto.Cipher import AES, RSA
from Crypto.Random import get_random_bytes
from socket import *
from Common import common
import os
import random


#enc_list = ["AES-256", "AES-196", "AES-128"]


class client(common): 
    def __init__(self, end, portNumber):
        super().__init__(end, portNumber)
        self.portNumber = portNumber #client's port number
        self.serverPN = 12000 #server's port number
        self.socket = socket(AF_INET, SOCK_DGRAM) #Creating a socket for the server. Connection type is UDP, and the IP protocol is IPv4.
        self.socket.bind(('127.0.0.1',self.portNumber)) #Binding the socket to the port number of the client.
    
    def sending(self):
        
        #the "e" is a flag and it's stand for encryption. The format is: e + "an encryption algorithm"
        enc_algo = "e AES-256" 
        super().sending(enc_algo, self.socket, self.serverPN)   
        
        recv_msg = self.receiving()
        addr = recv_msg[1]
        recv_msg = recv_msg[0].decode()
        
        if recv_msg == "eAck": 
            #creating the cipher suite
            symKey = get_random_bytes(32) # generating the key for AES-256
            cipher = AES.new(symKey, AES.MODE_GCM) 
            nonce = cipher.nonce

            """
            Sending the format of the message to the server. This allows to know the format of the file.
            Can change it to other file formats such as jpg or mp4.
            """
            format = input("Enter the format of the message (e.g txt): ")
            super().sending(f'f {format}', self.socket, self.serverPN) 

            super().sending(symKey, self.socket, self.serverPN) #Sending the nonce to the server. The nonce is needed for decryption.
            super().sending(nonce, self.socket, self.serverPN) #Sending the nonce to the server. The nonce is needed for decryption.

            try:
                #reading an sending the message in chunks of 4096 bytes
                with open(f"message.{format}", "rb") as f: 
                    while True:
                        rChunks = f.read(4096) 
                        enc_chunks = cipher.encrypt(rChunks) #Encrypting the message using the cipher suite. The message is encrypted in chunks of 4096 bytes.
                        if not rChunks:
                            break        

                        super().sending(enc_chunks, self.socket, self.serverPN) #Sending the message to the server.

            except Exception as e:
                super().sending("0", self.socket, self.serverPN) #If the file could not be opened, send an end-of-service flag to the server.
                print(f"Could not open file. Error: {e}")
            

        super().sending("0", self.socket, self.serverPN) #Always send an end-of-service flag to the server after sending the message.
                
    def receiving(self):
        #Receiving a packet from the server. If a packet is received, the client will print the message.

        message =  super().receiving(self.socket) 
        return message
    
    def close(self):
        return self.socket.close()

if __name__ == "__main__": 

    clientProgram = client("client", 12001)
    clientProgram.sending()
    clientProgram.close()
    
    
    