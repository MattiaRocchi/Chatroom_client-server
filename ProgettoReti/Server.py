import socket
import threading

# Lista per memorizzare i client connessi e i nicknames
clients = []
nicknames = []

# Funzione per gestire i messaggi dai client
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message: #Se il messaggio è presente lo manda in broadcast a tutti gli altri client
                broadcast(message, client_socket)
            else:
                remove_client(client_socket)
                break
        except:
            remove_client(client_socket)
            break

# Funzione per inviare messaggi a tutti i client tranne quello da cui partono
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove_client(client)

# Funzione per inviare la lista dei nickname a tutti i client
def send_nicknames():
    nicknames_list = "LISTNICK" + ",".join(nicknames) #Uso LISTNICK come codice per la lettura dei nick online
    print(nicknames_list)
    for client in clients:
        client.send(nicknames_list.encode('utf-8'))

# Funzione per rimuovere i client
def remove_client(client_socket):
    if client_socket in clients:
        index = clients.index(client_socket)
        clients.remove(client_socket)
        client_socket.close()
        nickname = nicknames[index]
        nicknames.remove(nickname)
        send_nicknames() #Rimanda i nick aggiornati

# Configurazione del server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 53000))
server.listen(5)
print("Server started and listening for connections...")

# Accettazione dei client
while True:
    client_socket, addr = server.accept()
    print(f"Connessione riuscita con: {addr}")
    
    nickname = client_socket.recv(1024).decode('utf-8') #Ottiene i nickdel client loggato anche ripetitivo

    #Aggiungo in lista le informazioni dell'utente appena connesso
    nicknames.append(nickname)
    clients.append(client_socket)

    print(f'Nickname dell utente è {nickname}')
    broadcast(f'{nickname} è online!', client_socket)
    send_nicknames()

    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()