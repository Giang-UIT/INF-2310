from Crypto.Cipher import AES
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
            #symKey = get_random_bytes(32) # generating the key for AES-256

            #cipher = AES.new(symKey, AES.MODE_GCM) #creating cypher object
            #cipherTxt, auth_tag = cipher.encrypt_and_digest(rChunks) #encrypts the message 
            #nonce = cipher.nonce #Storing the nonce

            with open ("message.txt", "rb") as f: #Writing 
                while True:
                    rChunks = f.read(4096) #Reading the message in chunks of 4096 bytes           
                    

                    if not rChunks:
                        break        

                    self.socket.sendall(rChunks, ('127.0.0.1', self.serverPN)) #Sending the message to the server.
                
                    
            
                
        
    def receiving(self):
        #Receiving a packet from the server. If a packet is received, the client will print the message.

        message =  super().receiving(self.socket) 
        #print(f"the client is receiving an incomming packet with the message being: {message[0].decode()}")
        
        return message
    
    def close(self):
        return self.socket.close()

if __name__ == "__main__": 

    clientProgram = client("client", 12001)
    clientProgram.sending()
    clientProgram.close()
    
    
    