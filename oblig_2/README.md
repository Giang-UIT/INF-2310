# How to run 

1) Run the server in a terminal (*python server.py*)  
2) Run the client in a seperate terminal (*python client.py*)

Once finished, a new file with the name "*recv_file.(the-chosen-format)*" will appear. 
That is the transfered file. 

--- 
# what has been changed? 

1) Now it is the server that does the encryption and sending the encrypted file. The client is the one that does the decryption.

2) The test variables from server are moved to client and vice versa.

3) Test program can now test whichever program by taking input.

4) Restructured the folder to match description and added a method for finding path because of the restructuring

5) Added print methods to print the test result to terminal

**Diagram of the interaction**

- This assumes that the interaction runs without errors. Exception handling is still a part of both programs. Test program is also there to detect errors. 


![alt text](image.png)
