import pytest
from client import client as c
from server import server as s


def test_client(): 
    client = c("client", 12001, True)
    
    client.sending()
    client.close()
    
    assert client.fAck == True
    assert client.eAck ==  True
    assert client.aesCheck == True



def test_server(): 
    server = s("server", 12000, True)
    server.listening()
    
    assert server.eFlagCheck == True
    assert server.fFlagCheck == True
    assert server.rsaCheck == True
    
    with open("message.txt", "rb") as f: 
        originalMsg = f.read()
    
    assert server.recvMsg == originalMsg
    
    server.close()

    
if __name__ == "__main__":
    
    testProgram = input("chose a number to test a program. 0 for client or 1 for server: ")
    


    if testProgram == "0": 
        
        test_client()
    elif testProgram == "1":
        test_server()