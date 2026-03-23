from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
import rsa
from socket import *
from Common import common



#enc_list = ["AES-256", "AES-196", "AES-128"]

class client(common): 
    def __init__(self, end: str, portNumber: int, testMode: bool):
        super().__init__(end, portNumber,testMode)
        self.portNumber = portNumber 
        self.serverPN = 12000 
        self.socket = socket(AF_INET, SOCK_DGRAM) #Creating a socket for the server. Connection type is UDP, and the IP protocol is IPv4.
        self.socket.bind(('127.0.0.1',self.portNumber)) #Binding the socket to the port number of the client.
        self.flags = ["e","f"]
        self.encList = ["AES-256", "RSA", "AES-196", "AES-128"]
        
        #Only for pytest
        self.eAck = False
        self.fAck = False
        self.rsaCheck = False
        self.aesCheck = False

        self.recv_msg =""
        self.testMode = testMode

       
    def sending(self):
        
        "==========================================================Sending cipher suite ========================================================================================="
        
        #the "e" is a flag that initiates the decision of encrypt algorithm. The format is: e + "an encryption algorithm"
        #super().sending(self.flags[0], self.socket, self.serverPN)   
        
        #Sendin the cipher suite. Requesting the server to use AES-256 and RSA
        enc_algo = f"{self.flags[0]} AES-256"
        super().sending(enc_algo, self.socket, self.serverPN)   
        enc_algo = f"{self.flags[1]} RSA"
        super().sending(enc_algo, self.socket, self.serverPN)   
        
        #expecting eAck
        recv_pk = self.receiving()
        
        if recv_pk[0] == b"eAck": 
            self.eAck = True
  
        else:
            raise Exception(f"the received message is not eAck. It is {recv_pk}")
        
        "===========================================================Sending file format==========================================================================================="


        """
        Sending the requested file and its format to the server. The inclusion of the format allows the server to know the format of the file.
        Can change it to other file formats such as jpg or mp4.
        """

        #format = input("Enter the format of the message (e.g txt): ")
        format = 'txt'
        req_file = f"file.{format}"
        super().sending(f'f {req_file}', self.socket, self.serverPN) #TODO: decrypts the request file
        
        #After receiving fAck, the client should receive symKey and nonce, and the file thereafter.
        recv_pk = self.receiving()

        if recv_pk[0] == b"fAck": 
          
            self.fAck = True
            recv_pk = self.receiving()

            try: 
                with open("private.pem", "rb") as f:
                    private_key = rsa.PrivateKey.load_pkcs1(f.read())
                    
                #Decrypting the package with the RSA algorithm. Expecting symKey and nonce in the same package
                dec_pkg = rsa.decrypt(recv_pk[0], private_key)
                print(dec_pkg)      
                symKey = dec_pkg[:32]
                nonce = dec_pkg[32:] #Receiving the nonce from the server. The nonce is needed for decryption.
                
                decipher = AES.new(symKey, AES.MODE_GCM, nonce=nonce)
                self.rsaCheck = True
                self.aesCheck = True

                with open (f"recv_file.{format}", "wb") as f: #Writing 
            
                    enChunks = self.receiving() #Receiving chunks of the encrypted file from the server.   

                    f.write(decipher.decrypt(enChunks[0])) #Writing the decrypted chunk to disk.
                        
                
                with open(f"recv_file.{format}", "rb") as f: 
                    self.recvMsg = f.read(4096)
                    
            except Exception: 
                raise Exception("Could not decrypt the file")
            
        else: 
            raise Exception(f"the received message is not fAck. It is {recv_pk}")
    
        super().sending("0", self.socket, self.serverPN) #Always send an end-of-service flag to the server after sending the message.
                
    def receiving(self):
        #Receiving a packet from the server. If a packet is received, the client will print the message.

        message =  super().receiving(self.socket) 
        return message
    
    def close(self):
        return self.socket.close()

if __name__ == "__main__": 

    clientProgram = client("client", 12001, False)
    clientProgram.sending()
    clientProgram.close()
    
    
    