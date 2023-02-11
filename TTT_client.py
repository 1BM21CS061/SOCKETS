#!/usr/bin/env python3

import time
import socket
import pickle

HOST = "192.168.11.233"  # The server's hostname or IP address
PORT = 25698  # The port used by the server

TTT = [[0,0,0],[0,0,0],[0,0,0]]
check = 0

def print_board(TTT):
    for i in TTT:
        print(i)

def recv():
    data = s.recv(4096)
    global TTT
    TTT = pickle.loads(data)
    #print(f"Received {data!r}")
    print_board(TTT)

    return data

def win_or_pass(r,c,k=1):
    global TTT 
    global check
    check = 0
    
    for i in range(3):
        if(TTT[i][c]==k):
            check=1 
            continue 
        else:
            check=0 
            break

    if(check==0):
        for i in range(3):
            if(TTT[r][i]==k):
                check=1
                continue 
            else:
                check=0
                break

    if(check==0 and r==c):
        for i in range(3):
            if(TTT[i][i]==k):
                check=1
                continue
            else:
                check=0
                break 

    if(check==0 and r+c==2):
        for i in range(3):
            if(TTT[i][2-i]==k):
                check=1
                continue 
            else:
                check=0 
                break 

def send_msg(sock):
    # Prefix each message with a 4-byte length (network byte order)
    row,column=input().split()
    row = int(row)
    column = int(column)
    global TTT 
    TTT[row][column]=2 
    move = pickle.dumps(TTT)
    win_or_pass(row,column)
    #msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(move)



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    #s.sendall(b"Hello, world")
    try:
        for i in range(4):
            if(check==1):
                print("You won")
                break
            else:
                recv()

                send_msg(s)
        

    except Exception:
        if(check==0):
            print("draw")
        else:
            print("You lost")
            
        
        
    
    '''data = s.recv(4096)
    TTT = pickle.loads(data)
    #print(f"Received {data!r}")
    print_board(TTT)'''

   
  


