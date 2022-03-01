import socket
import threading

nickname = input("Zvolte si prezdivku: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      
client.connect(('127.0.0.1', 22222))                             

def receive():
    while True:                                                 
        try:
            message = client.recv(1024).decode('UTF-8')
            if message == 'NICKNAME':
                client.send(nickname.encode('UTF-8'))
            else:
                print(message)
        except:                                                 
            print("Nastala chyba!")
            client.close()
            break

def write():
    while True:                                                 
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('UTF-8'))

receive_thread = threading.Thread(target=receive)               
receive_thread.start()
write_thread = threading.Thread(target=write)                   
write_thread.start()