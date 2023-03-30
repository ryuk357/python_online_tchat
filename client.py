import socket
import threading

"""
hote -> ip du serveur chat
port -> port utilise par le serveur chat
creation du socket de connexion et etabli la connexion
"""
hote = "192.168.1.14"
port = 6666
connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
print(f"Connexion établie avec le serveur sur le port {port}")
"""
boucle pour envoyer les messages vers le serveur
"""
def envoyer_messages(connexion):
    while True:
        message = input("> ")
        # Échapper les guillemets doubles
        message = message.replace('"', '\\"')
        # encode en bytes
        message = message.encode()
        connexion.send(message)
"""
Boucle pour receptionner les messages 
"""
def recevoir_messages(connexion):
    while True:
        message = connexion.recv(1024)
        print(message.decode())

"""
creation de 2 threads, un pour l'envoi de message, l'autre pour la reception

"""
thread_envoi = threading.Thread(target=envoyer_messages, args=(connexion_avec_serveur,))
thread_reception = threading.Thread(target=recevoir_messages, args=(connexion_avec_serveur,))

#demarrage des threads
thread_envoi.start()
thread_reception.start()

#empeche la perte  de messages -> join() -> permet d'attendre que le threads se termine correctement
thread_envoi.join()
thread_reception.join()

print("Fermeture de la connexion")
connexion_avec_serveur.close()