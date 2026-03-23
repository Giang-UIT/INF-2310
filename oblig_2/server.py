from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
import rsa
from socket import *
from Common import common




#Child class that inherits from parent class
class server(common): 
    def __init__(self, end, portNumber, testMode: bool):
        super().__init__(end, portNumber, testMode)
        self.portNumber = portNumber 
        self.socket = socket(AF_INET, SOCK_DGRAM) #Creating a socket for the server. Connection type is UDP, and the IP protocol is IPv4.
        self.socket.bind(('127.0.0.1',self.portNumber)) #Binding the socket to the port number of the server.
        self.encList = ["AES-256", "RSA", "AES-196", "AES-128"]
        self.fileFormats = ["txt", "jpg", "mp4"]
        self.chosenFormat = " "
        
        
        #For testing
        
        #self.deCheck = False
        self.eFlagCheck = False
        self.fFlagCheck = False

        self.testData = b"This is a test message"
        self.encTestMsg = ""
        self.deTestMsg = ""
        self.testMode = testMode

    
    def gen_RSA(self):
        public_key, private_key = rsa.newkeys(2048) 

        
        #Uses .pem so to pretend that they require password to access
        with open("public.pem", "wb") as f: 
            f.write(public_key.save_pkcs1("PEM"))
        
        with open("private.pem", "wb") as f:
            f.write(private_key.save_pkcs1("PEM"))

    
    def listening(self): 
        #Listening for incoming packets from the client. If a packet is received, the server will send an acknowledgment message back to the client.
        
        while True:
            packet = self.receiving() 

            if packet != None and packet != "0":
                self.sending(packet)
                
            elif packet == "0":

                #Shutting down if flag "0".
                print(f"Server received end-of-service flag. Closing connection and shutting down.")
                break
            

            
    def sending(self, packet):
        
        return super().sending(packet[0], self.socket,packet[1][1]) #Sending the message to the port number of the client that sent the packet to the server.
    
    def receiving(self): 
    #Receiving a request from the client. The server will prepare the file and sends it

        #unpacking the flags
        Packet =  super().receiving(self.socket)
    
        addr = Packet[1]
        Packet = Packet[0].decode()
        
        #if "e" flag is discovered, returns an ACK msg. 
        if Packet[0][0] == "e":     
            
            self.eFlagCheck = True
            
            newPacket = None
            enc_algo1 = Packet[2:] 
            
            enc_algo2 = super().receiving(self.socket)
            enc_algo2 = enc_algo2[0].decode()
            enc_algo2 = enc_algo2[2:]
            
            
            for algo in self.encList: 
                if enc_algo1 == algo:
                    flag = "e"
                elif enc_algo2 == algo: 
                    flag += "Ack"
                    newPacket = (flag, addr)
            
            return newPacket
            
                    
        elif Packet[0][0][0] == "f": #file flag. Flag for requested file. 
            self.fFlagCheck = True
            
            #Extracting the file of the message. The format is sent by the client before sending the message. This allows to know the format of the file.
            format = Packet[7:]
            
            newPacket = None
            
            for fileFormat in self.fileFormats: 
                if format == fileFormat: 
                    newPacket = ("fAck", addr)    
                    self.chosenFormat = fileFormat
                    self.sending(newPacket)
                    break

            if self.testMode == True:

                #Encryption test
                decipher = AES.new(symKey, AES.MODE_GCM, nonce=nonce)
                self.encTestMsg  = cipher.encrypt(self.testData)
                self.deTestMsg  = decipher.decrypt(self.encTestMsg)
                
                if self.deTestMsg == self.testData: 
                    self.encCheck = True
                    
            self.gen_RSA() #generating the RSA key pair for the client. The RSA key pair is needed for encryption and decryption of the symmetric key.
            
            symKey = get_random_bytes(32) #generating the key for AES-256
            cipher = AES.new(symKey, AES.MODE_GCM) 
            nonce = cipher.nonce

            with open("public.pem", "rb") as f: 
                public_key = rsa.PublicKey.load_pkcs1(f.read())
            
            enc_pkg = rsa.encrypt(symKey+nonce, public_key) #Encrypting the symmetric key with the RSA algorithm.
            
            self.sending((enc_pkg,addr)) #Sending the encrypted symmetric key to the client server.

            try:
                #sending the message in encrypted chunks of 4096 bytes
                with open(f"file.{format}", "rb") as f: 
                    while True:
                        rChunks = f.read(4096) 
                        enc_chunks = cipher.encrypt(rChunks)
                        
                        if not rChunks:
                            break        

                        self.sending((enc_chunks,addr))
                        return 

            except Exception as e:
                print(f"Something went wrong while trying to send the file. Error: {e}")

        elif Packet[0][0][0] == "0": #end-of-service flag
            return "0"     
            
    def close(self):
        return self.socket.close()

    
if __name__ == "__main__": 
    
    serverProgram = server("server", 12000, False)
    serverProgram.listening()
    serverProgram.close()
    