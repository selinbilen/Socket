#################################################
#I made a buzzer array
#first input is buzzer it calculates wich player is going to answer
#the second input is the answer
#Answers should be capital inputs "ABCD"
##################################################
import socket
import select
import random
import json
from thread import *
import sys
import time
from __main__ import *

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

ip =   "127.0.0.1"
#ip = ct[0]

########### PART FOR GUI ##########
# This part should be uncommented
# It only takes the port host and quiz name
"""
host = ct[0]
port = int(ct[1])
filename = ct[2]
"""
########### PART FOR GUI ##########

########### PART W/O GUI ##########
#"""
host = raw_input("Enter the host: ")
port = int(raw_input("Enter the port number to bind with: "))
filename = raw_input("Enter the quiz name:  ")
#"""
"""
filename = "questions.json"
host = 'localhost'
port = 1111
"""
########### PART W/O GUI ##########

s.bind((host, port))

s.listen(50)

score = [0, 0]

client_list = []
question = []
selections_a = []
selections_b = []
selections_c = []
selections_d = []
answer = []
cnt = []
username= []
number = len(question)
client = ["address", -1]


buzzer = [0,0,0]



with open(filename, 'r') as data:
    f = json.load(data)



j = random.sample(range(0, len(f)), 5)
#print j
for i in range(5):
    question.append(f[j[i]]["question"])
    selections_a.append(f[j[i]]["a"])
    selections_b.append(f[j[i]]["b"])
    selections_c.append(f[j[i]]["c"])
    selections_d.append(f[j[i]]["d"])
    answer.append(f[j[i]]["answer"])

"""
print question
print answer
print selections_a
print selections_b
print selections_c
print selections_d
"""
print("Waiting for players... ")
#conn, addr = server.accept()
#print("Player 1 has connected... ")
#conn.send("Welcome to the quiz\n".encode())
#conn.send("We still need one more player".encode())

#conn1, addr1 = server.accept()
#print("Player 2 has connected... ")
#conn1.send("Welcome to the quiz\n".encode())


def bdcast(message):
    for client in client_list:
        client.send(message)

def bodcast(message, client):
    client.send(message)
  
def thread_cli(conn, addr):
    #conn.send("Welcome to the quiz\n".encode())
    if len(client_list) ==1:
        conn.send("\nYou are the Player 1\n".encode())
        conn.send("We still need one more player...\n".encode())
    #conn.send("The only rule is to be faster than your opponent.\n".encode())
    while 2==2:
        message = conn.recv(2048)
        
        if buzzer[0] != 1 and buzzer[0]<1 :
            client[0] = conn
            buzzer[0] = 1
            i = 0
            k = len(client_list)
            while k > i:
                if client_list[i] != client[0]:
                    i +=1
                else:
                    break
            client[1] = i
            
        elif conn == client[0] and buzzer[0] == 1:
            right = (message[0] == answer[buzzer[2]][0])
            wrong = (message[0] != answer[buzzer[2]][0])
            #prints the correct answers to the server
            print answer[buzzer[2]][0]
            if right:
                bodcast("Correct Answer\n", client[0])
                cnt[i] += 10
            
            if wrong:
                bodcast("WRONGGG!!\n", client[0])
                cnt[i] -= 0
                
            buzzer[0]=0
            
            if len(question) != 0:
                question.pop(buzzer[2])
                selections_a.pop(buzzer[2])
                selections_b.pop(buzzer[2])
                selections_c.pop(buzzer[2])
                selections_d.pop(buzzer[2])
                answer.pop(buzzer[2])
                
            if len(question) == 0:
                bdcast("\n\nGAME OVER!\n")
                for j in range(0,1):
                    if cnt[j] == cnt[j+1]:
                        bdcast("\n\nIts a TIE\n")
                buzzer[1] = 1
                i = cnt.index(max(cnt))
                for j in range(0,1):
                    if cnt[j] != cnt[j+1]:
                        bdcast("Player " + str(i+1) + " WINS!! by scoring "+ str(cnt[i]) + " points.\n")
                        for x in range(len(client_list)):
                            client_list[x].send("You scored " + str(cnt[x]) + " points.")
                s.close()
            if len(question) !=0:
                buzzer[2] = random.randint(0,10000)%len(question)
                for connection in client_list:
                    connection.send("\n" +question[buzzer[2]] + "\n\n")
                    connection.send("A: " + selections_a[buzzer[2]] + "\n")
                    connection.send("B: " + selections_b[buzzer[2]] + "\n")
                    connection.send("C: " + selections_c[buzzer[2]] + "\n")
                    connection.send("D: " + selections_d[buzzer[2]] + "\n")
        else:
            conn.send(" Player " + str(client[1]+1) + " pressed first\n")

def server():
    while 2==2:
        conn, addr = s.accept()
        client_list.append(conn)
        cnt.append(0)
        print "Player " + str(len(cnt)) + " connected "
        start_new_thread(thread_cli,(conn, addr))
        if (len(client_list) == 2 or len(client_list) > 2):
            if len(question) !=0:
                buzzer[2] = random.randint(0,10000)%len(question)
            
                for connection in client_list:
                    connection.send("\n" +question[buzzer[2]] + "\n\n")
                    connection.send("A: " + selections_a[buzzer[2]] + "\n")
                    connection.send("B: " + selections_b[buzzer[2]] + "\n")
                    connection.send("C: " + selections_c[buzzer[2]] + "\n")
                    connection.send("D: " + selections_d[buzzer[2]] + "\n")
            
            
    conn.close()
    s.close()

    
server()
