import socket
import sys
from re import search
from socket import *
import re

INSERT_PATTERN = "^1\s[\s0-9\s]*\s[a-zA-Z_.,-;]+$"  # TODO fix the regex!!!
SEARCH_PATTERN = "^2\s[\s0-9\sa-zA-Z_.,-=)(]+$"  # TODO fix the regex!!!

'''
Class Name: Handler
Args type: data, socket, set_val
Return Val: None
Info: Handel's Clients data
'''


class Handler:
    def __init__(self, data, socket, set_val):
        self.data = data
        self.socket = socket
        self.set_val = set_val

    '''
    Name: manage 
    Args type: None
    Return Val: None
    Info: Manage client's input- registration and search 
    '''

    def manage(self):
        # File registration
        if re.match(INSERT_PATTERN, self.data):
            self.set_val.process(self.data)
        # File search
        if re.match(SEARCH_PATTERN, self.data):
            self.set_val.search(self.data, self.socket)


'''
Class Name: Manager
Args type: Client address
Return Val: None
Info: Manage Clients Info- what files he posses
'''


class Manager:

    def __init__(self, client_addr):
        self.dict = {}
        self.addr = client_addr

    '''
    Name: set
    Args type: key, value
    Return Val: None
    Info: Sets the dictionary
    '''

    def set(self, key, value):
        self.dict[key] = value

    '''
    Name: process
    Args type: data
    Return Val: None
    Info: Split and Parse the data for the dictionary
    '''

    def process(self, data):
        parse = str(data).split()
        value = str(self.addr[0]) + " " + parse[1]
        to_split = data[7:]
        list_of_keys = str(to_split).split(",")
        for i in range(len(list_of_keys)):
            self.set(list_of_keys[i], value)

    '''
    Name: search
    Args type: data , socket
    Return Val: None
    Info: Searches files name or sub-string of files name and send it 
    '''

    def search(self, data, socket):
        if self.dict is None:
            print("The word: " + str(data) + " don't exists - there is no such file name ")
        else:
            to_search = str(data[2:])
            msg = ""
            # sorts the massages to the client
            for k in sorted(self.dict.keys()):
                if to_search in k:
                    msg = msg + str(k) + " " + str(self.dict[k]) + " , "

            socket.send(msg[:len(msg) - 2].encode())


'''
Name: Main
Args type:
Return Val:
Info:
'''
if __name__ == "__main__":
    # if there is 4 args- go to the user mode '1'
    if len(sys.argv) is 4:
        if sys.argv[1] is not 0:
            print("Wrong argument- if you want to use, put '1' as the first arg")
            exit(0)

        server = socket(AF_INET, SOCK_STREAM)
        server_ip = "192.168.43.43"
        server_port = 8000
        server.bind((server_ip, server_port))
        server.listen(5)

        while True:
            client_socket, client_address = server.accept()
            data = client_socket.recv(1024)
            set_val = Manager(client_address)
            while not data == "":
                handler = Handler(data.decode(), client_socket, set_val)
                handler.manage()
                client_socket.send(data.upper())  # to fix
                data = client_socket.recv(1024)

            print("Client Disconnected")
            client_socket.close()
    # if there is 5 args- go to the listening mode '0'
    if len(sys.argv) is 5:
        if sys.argv[1] is not 0:
            print("Wrong argument- if you want to listen, put '0' as the first arg")
            exit(0)
    
    else:
        print("Problem with args - try again")
