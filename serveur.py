import socket
import threading

""" ip du serveur sur lequel est heberge le chat et du port qui sera utilise """
hote = "192.168.1.14"
port = 6666
"""
Creation d'un socket pour le serveur 
- AF_INET pour adresses IPV4
- SOCK_STREAM pour socket TCP
bind -> association du socket a l'ip et au port utilise
"""
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind((hote, port))

"""Ecouter les connexions entrantes sur le socket"""
serveur.listen()

print(f"Le serveur écoute à présent sur le port {port}")
"""Cette liste contiendra toutes les connexions client"""
clients = []

"""fonction qui va etre executee dans un thread et
qui sert a receptionner les messages et les redistribuer aux clients
"""
def gerer_client(connexion_client, adresse_client):

    #Ajout des connexions dans la liste clients
    clients.append(connexion_client)
    #Boucle indefiniment pour receptionner les msg et les distribuer
    while True:
        try:
            # Recevoir un message du client
            message = connexion_client.recv(1024).decode()
            if message:
                print(f"{adresse_client} : {message}")
                # Transmettre le message a tous les autres clients
                for client in clients:
                    if client != connexion_client:
                        client.send(f"{adresse_client} : {message}".encode())
            else:
                # Si le message est vide, supprimer la connexion client + sortir
                clients.remove(connexion_client)
                connexion_client.close()
                break
        except:
            # Si une erreur se produit, supprimer la connexion client + sortir
            clients.remove(connexion_client)
            connexion_client.close()
            break

"""Boucle pour accepter les connexions entrantes
 execute la fonction gerer_client et demarre le tread"""
while True:
    """
    Accepter une nouvelle connexion client
    addresse_client  = ('IP client',' port du client')
    connexion_client = <socket.socket fd=400, family=2, type=1, proto=0, laddr=('192.168.1.14', 6666), raddr=('192.168.1.14', 56440)>
    accept() est une méthode bloquante du socket qui attend qu'une connexion client se connecte au serveur.
    """
    connexion_client, adresse_client = serveur.accept()
    #print(adresse_client)
    #print(connexion_client)

    print(f"Connexion établie avec {adresse_client[0]}:{adresse_client[1]}")

    # creation d'un thread pour gérer la connexion client avec la methode qui sera executee
    thread_client = threading.Thread(target=gerer_client, args=(connexion_client, adresse_client))
    thread_client.start()
