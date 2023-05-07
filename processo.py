import socket
import time

HOST = 'localhost'
PORT = 5000

id_processo = int(input("Insira o ID do processo: "))

processo = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
processo.connect((HOST, PORT))

while True:
    processo.sendall(str(id_processo).encode())

    data = processo.recv(1024)

    if data.decode() == "OK":
        print(f"Processo {id_processo} tem acesso à região crítica")
        time.sleep(5)

        processo.sendall(b"RELEASE")

        print(f"Processo {id_processo} liberou o acesso à região crítica")
        break
    else:
        print(f"Processo {id_processo} aguardando o acesso à região crítica")
        time.sleep(2)
    
processo.close()