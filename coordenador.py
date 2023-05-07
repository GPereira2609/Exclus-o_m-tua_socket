import socket

from threading import Thread

HOST = 'localhost'
PORT = 5000

max_workers = 2

coordenador = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
coordenador.bind((HOST, PORT))
coordenador.listen(max_workers)

print(f"""
Ouvindo...
Host = {HOST}
Porta = {PORT}
""")

fila_processos = []
processo_atual = None

def processar_requisicao(processo):
    global fila_processos, processo_atual

    data = processo.recv(1024)
    id_processo = int(data.decode())

    print(f"Processo {id_processo} requsitando acesso à região crítica")

    if processo_atual is None:
        processo_atual = id_processo
        print(f"Processo {id_processo} recebeu acesso à região crítica")
        processo.sendall(b"OK")
    else:
        fila_processos.append(id_processo)
        print(f"Processo {id_processo} adicionado à fila de processos em espera")

    while True:
        if processo_atual == id_processo:
            processo.sendall(b"OK")
        else:
            processo.sendall(b"Aguarde")
            print(f"Processo {id_processo} aguardando acesso à região crítica")

        data = processo.recv(1024)
        if not data:
            break

        if data.decode() == "RELEASE":
            if processo_atual == id_processo:
                processo_atual = None
                print(f"Processo {id_processo} liberou acesso à região crítica")

                if fila_processos:
                    proximo_processo = fila_processos.pop(0)
                    processo_atual = proximo_processo
                    print(f"Processo {proximo_processo} recebeu acesso à região crítica")
            break
    print(f"Conexão fechada com o processo {id_processo}")
    processo.close()

while True:
    processo, ender = coordenador.accept()
    print(f"Conectado com {ender}")

    t = Thread(target=processar_requisicao, args=[processo])
    t.start()
