# Jesse Talamantes
# Project 3 - client side chat program
# Runnable via: python3 client.py

from socket import *
import sys
import select

login = False

# for testing
#user = "talamantes"
#pw = "p398"
#sName = 'cyberlab.pacific.edu'
#sPort = 12000

def main():
    attempt = 0
    sName = input("Please enter the server hostname: ")
    sPort = input("Please enter the server port number: ")
    print(sName, sPort)
    s = socket(AF_INET, SOCK_STREAM)

    try:
        s.connect((str(sName), int(sPort)))
    except:
        print("Incorrect server name and/or port.")
        sys.exit()

    while True:
        if auth(s, attempt):
            print("You are now authenticated.")
            login = True
            break
        else:
            print("Incorrect username and/or password. Retry")
        
        attempt = attempt+1

    socket_list = [0, s]

    prompt()

    while login:
        read, write, err = select.select(socket_list, [], [])
        
        for sock in read:
            if sock == s:
                data = sock.recv(2048)
                if not data:
                    print("Unexpected Disconnected!")
                    sys.exit()
                else:
                    if b'FROM' in data:
                        frum, user, msg1 = data.decode().split(":")
                        print("Message from",user,":", msg1)
                    elif b'SIGNIN' in data:
                        sign, user = data.decode().split(":")
                        user = user.rstrip('\r\n')
                        print(user, " signed on.")
                    elif b'SIGNOFF' in data:
                        sign, user = data.decode().split(":")
                        user = user.rstrip('\r\n')
                        print(user, " signed off.")
                    else:
                        print("Users currently logged in: \n", data.decode())
                        prompt()

            else:
                choice = sys.stdin.readline()
                choice = choice.rstrip('\r\n')
                if choice is "1":
                    listUsers(s)
                elif choice is "2":
                    msg(s)
                    prompt()
                elif choice is "3":
                    s.send(str.encode("BYE"))
                    sys.exit()
                else:
                    print("Invalid option. Try again.")
                    prompt()
                    continue  
    s.close()

def prompt():
    sys.stdout.write("Choose an option:\n1.\tList online users\n2.\tSend someone a message\n3.\tSign off\n")

def msg(s):
    to      = input("User you would like to message: ")
    userMsg = input("Message: ")

    fullMsgAsBytes = str.encode("TO:"+to+":"+userMsg)
    s.send(fullMsgAsBytes)
    print("Message sent")


def listUsers(s):
    s.send(str.encode("LIST"))


def auth(s, atmpt):
    user = input("Please enter a username: ")
    pw   = input("Please enter a password: ")

    if atmpt == 0:
        print("sending hello")
        s.send(str.encode("HELLO"))
        response = s.recv(2048)
    

    authAsBytes = str.encode("AUTH:"+user+":"+pw)

    s.send(authAsBytes)

    response = s.recv(2048)
    
    if b'AUTHYES' in response:
        signon = s.recv(2048) #to catch own signon msg
        return True
    else:
        return False
        


main()
