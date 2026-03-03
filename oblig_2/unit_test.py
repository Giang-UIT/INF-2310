import pytest
from client import client as c
from server import server as s

"""
def test_client(): 
    client = c("client", 12001, True)
    
    client.sending()
    client.close()
    
    assert client.fAck == True
    assert client.eAck ==  True
    assert client.encCheck == True
"""    


def test_server(): 
    server = s("server", 12000, True)
    server.listening()
    
    
    
    assert server.eFlagCheck == True
    assert server.fFlagCheck == True
    
    with open("message.txt", "rb") as f: 
        originalMsg = f.read()
    
    assert server.recvMsg == originalMsg
    
    server.close()
    
    
if __name__ == "__main__":
    
    #test_client()
    test_server()