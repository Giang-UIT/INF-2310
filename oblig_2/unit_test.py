import pytest
from client import client as c
from server import server as s


def clientTesting(): 
    client = c("client", 12001)
    
    client.sending()
    client.close()
    
    assert client.fAck == True
    assert client.eAck ==  True
    assert client.encCheck == True
    assert client.deCheck == True
    
    

def serverTesting(self, client: c, server: s): 
    server = s("server", 12000)
    server.listening()
    server.close()
    
    
if __name__ == "__main__":
    
    #test_integrity(client_test, server_test)
    #test_confindentiality(client_test, server_test)
    #test_availability(client_test, server_test)
    
    clientTesting()
    #serverTesting()