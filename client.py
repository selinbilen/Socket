import socket
import select
import sys
from __main__ import *
s = socket.socket()


########### PART FOR GUI ##########
"""
host = c[0]
port = int(c[1])
my_username = c[2]
"""
########### PART FOR GUI ##########


########### PART W/O GUI ##########
# This part should be uncommented
# It only takes the port host and quiz name
#"""
host = raw_input("Enter the host: ")
port = int(raw_input("Enter the port number to bind with: "))
my_username = raw_input("Username: ")
#"""
"""
host =  "127.0.0.1"
port = 1111
my_username = raw_input("Username: ")
"""
print("You are in " + my_username + " !" )
print("\nWelcome to the quiz\n")
print("The only rule is to be faster than your opponent.")
########### PART W/O GUI ###########


s.connect((host, port))
s.setblocking(False)

"""
message = s.recv(1024)
message = message.decode()
print (message)
"""

def client():
    while 1:
        socketlist = [sys.stdin, s]
        read ,write,error = select.select(socketlist,[],[])
      
        for sockets in read:
            if sockets != s:
                message = sys.stdin.readline()
                s.send(message)
                sys.stdout.flush()
            else:
                message = sockets.recv(2048)
                print message
    s.close()
    sys.exit()

client()
