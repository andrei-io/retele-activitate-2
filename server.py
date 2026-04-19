import socket

HOST        = '127.0.0.1'
PORT        = 9999
BUFFER_SIZE = 1024

clienti_conectati = {}
mesaje = {} # Structura: { id_mesaj: {'autor': adresa_client, 'text': "mesaj"} }
id_curent = 1

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print("=" * 50)
print(f"  SERVER UDP pornit pe {HOST}:{PORT}")
print("  Asteptam mesaje de la clienti...")
print("=" * 50)

while True:
    try:
        date_brute, adresa_client = server_socket.recvfrom(BUFFER_SIZE)
        mesaj_primit = date_brute.decode('utf-8').strip()

        parti = mesaj_primit.split(' ', 1)
        comanda = parti[0].upper()
        argumente = parti[1] if len(parti) > 1 else ''

        print(f"\n[PRIMIT] De la {adresa_client}: '{mesaj_primit}'")

        # Validare permisiune generala pentru comenzi restrictionate
        if comanda in ['PUBLISH', 'DELETE', 'LIST'] and adresa_client not in clienti_conectati:
            raspuns = "EROARE: Nu esti conectat la server"
            server_socket.sendto(raspuns.encode('utf-8'), adresa_client)
            continue

        if comanda == 'CONNECT':
            if adresa_client in clienti_conectati:
                raspuns = "EROARE: Esti deja conectat la server."
            else:
                clienti_conectati[adresa_client] = True
                nr_clienti = len(clienti_conectati)
                raspuns = f"OK: Conectat cu succes. Clienti activi: {nr_clienti}"
                print(f"[SERVER] Client nou conectat: {adresa_client}")

        elif comanda == 'DISCONNECT':
            if adresa_client in clienti_conectati:
                del clienti_conectati[adresa_client]
                raspuns = "OK: Deconectat"
                print(f"[SERVER] Client deconectat: {adresa_client}")
            else:
                raspuns = "EROARE: Nu esti conectat la server."

        elif comanda == 'PUBLISH':
            if not argumente:
                raspuns = "EROARE: Mesajul gol."
            else:
                mesaje[id_curent] = {'autor': adresa_client, 'text': argumente}
                raspuns = f"OK: Mesaj publicat cu ID={id_curent}"
                id_curent += 1

        elif comanda == 'DELETE':
            if not argumente or not argumente.isdigit():
                raspuns = "EROARE: Argumentul trebuie sa fie un numar."
            else:
                id_sters = int(argumente)
                if id_sters not in mesaje:
                    raspuns = f"EROARE: Mesaj."
                elif mesaje[id_sters]['autor'] != adresa_client:
                    raspuns = "EROARE: Nu ai permisiunea."
                else:
                    del mesaje[id_sters]
                    raspuns = f"OK: Mesajul cu ID={id_sters} a fost sters."

        elif comanda == 'LIST':
            if not mesaje:
                raspuns = "Nu exista mesaje publicate pe server."
            else:
                raspuns = "Lista mesaje:\n"
                for msg_id, detalii in mesaje.items():
                    raspuns += f"[{msg_id}] {detalii['text']}\n"


        else:
            raspuns = f"EROARE: Comanda '{comanda}' este invalida."

        server_socket.sendto(raspuns.encode('utf-8'), adresa_client)
        print(f"[TRIMIS]  Catre {adresa_client}: '{raspuns}'")

    except KeyboardInterrupt:
        print("\n[SERVER] Oprire server...")
        break
    except Exception as e:
        print(f"[EROARE] {e}")

server_socket.close()
print("[SERVER] Socket inchis.")