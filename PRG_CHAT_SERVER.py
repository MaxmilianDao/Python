#import knihoven
import socket
import threading                                                

#nastaveni IP
#nastaveni portu
host = '127.0.0.1'                                                      
port = 22222                                                             

#socket: class v socket modulu
#AF_INET: internetovy socket IPv4, SOCK_STREAM: TCP protokol
#passuje tuple host a port a nasledovne bindne 
# ¨posloucha¨ prichozi pripojeni
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              
server.bind((host, port))                                               
server.listen()

#list aktualne pripojenych klient
#list prezdivek aktualne pripojenych klientu
clients = []
nicknames = []


def broadcast(message):                                                 
    for client in clients:
        client.send(message)
#broadcasti prijate zpravy vsem
#pri ztrate pripojeni urciteho klienta broadcastne vsem klientum ze se dany klient odpojil
#pote klienta odebere a uzavre socket
def handle(client):                                         
    while True:
        try:                                                            
            message = client.recv(1024)
            broadcast(message)
        except:                                                         
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} se odpojil!'.format(nickname).encode('UTF-8'))
            nicknames.remove(nickname)
            break
#
def receive():                                                          
    while True:
        client, address = server.accept()
        print("Pripojeno adresou {}".format(str(address)))       
        nickname = client.recv(1024).decode('UTF-8')
        nicknames.append(nickname)
        clients.append(client)
        print("S prezdivkou {}".format(nickname))
        broadcast("{} se pripojil".format(nickname).encode('UTF-8'))
        client.send('Uspesne pripojeno!'.encode('UTF-8'))
        thread = threading.Thread(target=handle, args=(client))
        thread.start()
#volani funkce receive
receive()