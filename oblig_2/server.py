#! flask/bin/python3
from socket import *
from Crypto.Cipher import AES, PKCS1_OAEP
import rsa
from Common import common



#Child class that inherits from parent class
class server(common): 
    def __init__(self, end, portNumber):
        super().__init__(end, portNumber)
        self.portNumber = portNumber #server's port number
        self.socket = socket(AF_INET, SOCK_DGRAM) #Creating a socket for the server. Connection type is UDP, and the IP protocol is IPv4.
        self.socket.bind(('127.0.0.1',self.portNumber)) #Binding the socket to the port number of the server.
        self.encList = ["AES-256", "RSA", "AES-196", "AES-128"]
        self.fileFormats = ["txt", "jpg", "mp4"]
        self.chosenFormat = " "
    
    def listening(self): 
        #Listening for incoming packets from the client. If a packet is received, the server will send an acknowledgment message back to the client.
        
        while True:
            packet = self.receiving() 
            
            if packet == "0":
                print(f"Server received end-of-service flag. Closing connection and shutting down.")
                break

            elif packet != None:
                self.sending(packet)
                

            
    def sending(self, packet):
        
        
        return super().sending(packet[0], self.socket,packet[1][1]) #Sending the message to the port number of the client that sent the packet to the server.
    
    def receiving(self): #Receiving a packet from the client. If a packet is received, the server will return the packet
    
        #unpacking the package
        Packet =  super().receiving(self.socket)
        
        try:
            addr = Packet[1]
            Packet = Packet[0].decode()  
            
                #if "e" flag is discovered, returns an ACK msg. 
            if Packet[0][0] == "e":     
                
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
                
                        
            elif Packet[0][0][0] == "f": #format flag. 
                format = Packet[2:] #Extracting the format of the message. The format is sent by the client before sending the message. This allows to know the format of the file.
                newPacket = None
                
                for fileFormat in self.fileFormats: 
                    if format == fileFormat: 
                        newPacket = ("fAck", addr)    
                        self.chosenFormat = fileFormat
                        break
                    
                return newPacket
            
        except UnicodeDecodeError: #This assumes that the decode method tried to decode encrypted binaries
            
            with open("private.pem", "rb") as f:
                private_key = rsa.PrivateKey.load_pkcs1(f.read())
            
            pkg = rsa.decrypt(Packet[0], private_key) #Decrypting the package with the RSA algorithm. The package contains the symmetric key and nonce.

            symKey = pkg[:32]
            nonce = pkg[32:] #Receiving the nonce from the client. The nonce is needed for decryption.
            
            decipher = AES.new(symKey, AES.MODE_GCM, nonce=nonce)

            with open (f"recv_message.{self.chosenFormat}", "wb") as f: #Writing 
               
                while True:
                    mChunks = super().receiving(self.socket) #Receiving the message from the client.   
                    print(f"the {self.end} received message: {mChunks[0]}")
                    if mChunks[0] == b"0": #end-of-service flag.
                        return "0"

                    f.write(decipher.decrypt(mChunks[0])) #Writing the message to a file.
        
    def close(self):
        return self.socket.close()
    
    
    
    
             
if __name__ == "__main__": 
    
    serverProgram = server("server", 12000)
    serverProgram.listening()
    serverProgram.close()
    