import socket
import threading
import tkinter
from tkinter import simpledialog, Scrollbar

# Funzione per ricevere messaggi dal server
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message.startswith('LISTNICK'): #Controllo se devo stampare sulla gui la lista dei nickname o un messaggio
                message = message[8:]
                update_nickname_list(message)
            else:
                chat_box.config(state=tkinter.NORMAL)
                chat_box.insert(tkinter.END, message + '\n')
                chat_box.config(state=tkinter.DISABLED)
                chat_box.see(tkinter.END)
        except ConnectionResetError:
            print("Connessione persa.")
            client.close()
            break
        except Exception as e:
            print(f"Si è verificato un errore!: {e}")
            client.close()
            break

# Funzione per inviare messaggi al server
def send_message(event=None):
    try:
        message = f'{nickname}: {input_message.get()}'
        input_message.set("")
        # Mostra il messaggio anche nella chat del mittente
        client.send(message.encode('utf-8'))
        chat_box.config(state=tkinter.NORMAL)
        chat_box.insert(tkinter.END, message + '\n')
        chat_box.config(state=tkinter.DISABLED)
        chat_box.see(tkinter.END)
    except Exception as e:
        print(f"Si è verificato un errore nel inviare un messaggio: {e}")

# Funzione per aggiornare la lista dei nickname
def update_nickname_list(message):
    nicknames = message.split(',') #Ricreo la lista splittando nelle vergole
    nickname_box.config(state=tkinter.NORMAL)
    nickname_box.delete(1.0, tkinter.END)
    nickname_box.insert(tkinter.END, "Utenti Online:\n")
    for name in nicknames:
        nickname_box.insert(tkinter.END, name + '\n')
    nickname_box.config(state=tkinter.DISABLED)

# Funzione per chiudere la connessione del client
def on_closing(event=None):
    try:
        client.send(f'{nickname} ha lasciato la chat.'.encode('utf-8'))
        client.close()
    except Exception as e:
        print(f"Si è verificato un errore durante la disconnessione: {e}")
    finally:
        window.quit()

# Configurazione del client
server_ip = '127.0.0.1'
server_port = 53000

# Richiesta del nickname all'utente
window = tkinter.Tk()
window.withdraw()
window.geometry("650x550")

nickname = simpledialog.askstring("Nickname", "Choose your nickname (Possono essere presenti omonimi): ", parent=window)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, server_port))
client.send(nickname.encode('utf-8'))


# Configurazione della GUI 
window.deiconify()
window.title("Chatroom")
window.geometry("650x550")

main_frame = tkinter.Frame(window)
main_frame.pack(expand=True, fill='both')

# Frame per la chat
chat_frame = tkinter.Frame(main_frame)
chat_frame.pack(side=tkinter.LEFT, expand=True, fill='both')

chat_box = tkinter.Text(chat_frame, state='disabled', wrap=tkinter.WORD, width=30, height=10)
chat_box.pack(padx=5, pady=5, expand=True, fill='both')

# Scrollbar per la chat
chat_scrollbar = Scrollbar(chat_box, command=chat_box.yview)
chat_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
chat_box['yscrollcommand'] = chat_scrollbar.set

# Frame per la lista dei nickname
nickname_frame = tkinter.Frame(main_frame, width=100)
nickname_frame.pack(side=tkinter.LEFT, fill='both')

nickname_box = tkinter.Text(nickname_frame, state='disabled',wrap=tkinter.WORD, width=15, height=10)
nickname_box.pack(padx=5, pady=5, expand=True,  fill='both')

# Scrollbar per la lista dei nickname
nickname_scrollbar = Scrollbar(main_frame, command=nickname_box.yview)
nickname_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
nickname_box['yscrollcommand'] = nickname_scrollbar.set

# Frame per l'input
input_frame = tkinter.Frame(window)
input_frame.pack(fill='x')

input_message = tkinter.StringVar()
input_field = tkinter.Entry(input_frame, textvariable=input_message)
input_field.pack(side='left', padx=5, pady=5, expand=True, fill='x')
input_field.bind("<Return>", send_message)

send_button = tkinter.Button(input_frame, text="Send", command=send_message)
send_button.pack(side='right', padx=5, pady=5)

window.protocol("WM_DELETE_WINDOW", on_closing)

# Mostra l'entrata in chat all'avvio
chat_box.config(state=tkinter.NORMAL)
chat_box.insert(tkinter.END, "Sei entrato in chat con il seguente nickname:" + nickname + "\n")
chat_box.config(state=tkinter.DISABLED)

# Thread per ricevere messaggi
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Avvio della GUI
window.mainloop()