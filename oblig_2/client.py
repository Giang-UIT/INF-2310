from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
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
        self.flags = ["e","f"]
        
        
        #Only for pytest
        self.eAck = False
        self.fAck = False
        self.encCheck = False
        self.deCheck = False
        self.testData = b"This is a test message"
        self.encTestMsg = ""
        self.deTestMsg = ""

    def gen_RSA(self):
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        
        #Pretends that they require password to access
        with open("public.txt", "wb") as f: 
            f.write(public_key)
        
        with open("private.txt", "wb") as f:
            f.write(private_key)

        return private_key, public_key
    
    def sending(self):
        
        "==========================================================Sending cipher suite ========================================================================================="
        
        #the "e" is a flag that initiates the decision of encrypt algorithm. The format is: e + "an encryption algorithm"
        #super().sending(self.flags[0], self.socket, self.serverPN)   
        
        enc_algo = f"{self.flags[0]} AES-256"
        super().sending(enc_algo, self.socket, self.serverPN)   
        enc_algo = f"{self.flags[1]} RSA"
        super().sending(enc_algo, self.socket, self.serverPN)   
        
        recv_msg = self.receiving()
        
        
        if recv_msg[0].decode() == "eAck": 
            
            RSA_keys = self.gen_RSA() #generating the RSA key pair for the client. The RSA key pair is needed for encryption and decryption of the symmetric key.
            
            #creating the cipher suite
            symKey = get_random_bytes(32) # generating the key for AES-256
            cipher = AES.new(symKey, AES.MODE_GCM) 
            nonce = cipher.nonce
           
            self.eAck = True
            
  
        else :
            raise Exception(f"the received message is not eAck. It is {recv_msg}")
        
        "===========================================================Sending file format==========================================================================================="
                  
        """
        Sending the format of the message to the server. This allows to know the format of the file.
        Can change it to other file formats such as jpg or mp4.
        """
        
        format = input("Enter the format of the message (e.g txt): ")
        super().sending(f'f {format}', self.socket, self.serverPN) 
        
        recv_msg = self.receiving()
        
        self.sending = 0
        
        if recv_msg[0].decode() == "fAck": 
            
            #After receiving fAck, the client send symKey and nonce, and the file thereafter. 
            self.fAck = True
            
            super().sending(symKey, self.socket, self.serverPN) #Sending the symmetric key to the server. The nonce is needed for decryption.
            super().sending(nonce, self.socket, self.serverPN) #Sending the nonce to the server. The nonce is needed for decryption.
            
            
            decipher = AES.new(symKey, AES.MODE_GCM, nonce=nonce)
            self.encTestMsg  = cipher.encrypt(self.testData)
            self.encCheck = True
            self.deTestMsg  = decipher.decrypt(self.encTestMsg)
            self.deCheck = True
            
            try:
                #sending the message in encrypted chunks of 4096 bytes
                with open(f"message.{format}", "rb") as f: 
                    while True:
                        rChunks = f.read(4096) 
                        enc_chunks = cipher.encrypt(rChunks)
                        
                        
                        if not rChunks:
                            break        

                        super().sending(enc_chunks, self.socket, self.serverPN)

            except Exception as e:
                print(f"Something went wrong while trying to send the file. Error: {e}")
                super().sending("0", self.socket, self.serverPN) #If the file could not be opened, send an end-of-service flag to the server.
                
            
        else: 
            raise Exception(f"the received message is not fAck. It is {recv_msg}")

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
    
    
    