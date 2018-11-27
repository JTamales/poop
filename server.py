# Jesse Talamantes
# Project 4 - server side chat program
# Runnable via: python3 server.py
# Connect to the server with the host: localhost and port: 12346

from socket import *
import sys
import select
import _thread

server_socket = socket(AF_INET, SOCK_STREAM) 
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) 

# server info
host    = "localhost"
port    = 12346

listOfClients = []
listOfUsers   = []

server_socket.bind((host, port)) 

server_socket.listen(100)

listOfClients.append(server_socket)

def newClient(conn, addr):
    while True:
        try:
            data = conn.recv(2048)
            if data:
                #parse and determine what they sent
                if b'HELLO' in data:
                    conn.send(str.encode("HELLO"))
                    while True:
                        auth = conn.recv(2048)
                        if b'AUTH:' in auth:
                            ath, user, pw = auth.decode().split(":")
                            print(user, " logged in")
                            listOfUsers.append((user, conn))
                            conn.send(str.encode("AUTHYES"))
                            signMsg = "SIGNIN:" + user
                            broadcast(signMsg, server_socket)
                            break
                        else:
                            conn.send(str.encode("AUTHNO"))
                elif b'LIST' in data:
                    users = ""
                    for u, c in listOfUsers:
                        users = u + ", " + users
                    print(users)
                    conn.send(str.encode(users))
                elif b'BYE' in data:
                    print(user, "signed off")
                    signMsg = "SIGNOFF:" + user
                    broadcast(signMsg, server_socket)
                elif b'TO:' in data:
                    to, toUser, usrMsg = data.decode().split(":")
                    print("sending msg from ", user, " to ", toUser)
                    usrMsg = "FROM:"+user+":"+usrMsg
                    for u, c in listOfUsers: 
                        if u==toUser: 
                            c.send(str.encode(usrMsg))
            else:
                remove(conn)
                listOfUsers.remove((user, conn))
                break
        except:
            continue

def broadcast(msg, conn): 
    for clients in listOfClients: 
        if clients!=conn: 
            try: 
                clients.send(str.encode(msg))
            except: 
                clients.close() 
  
                # if the link is broken, we remove the client 
                remove(clients) 

def remove(conn): 
    if conn in listOfClients: 
        listOfClients.remove(conn)

while True: 
        conn, addr = server_socket.accept() 
        listOfClients.append(conn)
        print(addr, "Connected")
        _thread.start_new_thread(newClient, (conn, addr))

            
server_socket.close() 
conn.close()