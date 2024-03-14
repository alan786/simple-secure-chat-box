# Importing functions for the server programming
import socket
import ssl
import threading

# Importing functions for encryption/decryption through Python's cryptography functions
import codecs
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Dictionary to store clients and their nicknames
clients = {}

# Function to broadcast messages to all connected clients
def broadcast(message, sender_socket):
    for client_socket, nickname in clients.items():
        if client_socket != sender_socket:
            try:
                client_socket.send(f"{sender_socket}: {message}".encode('utf-8'))
            except:
                # Remove disconnected client
                remove_client(client_socket)

# Function to handle each client's connection
def handle_client(client_socket):
    ssl_socket = None  # Initialize ssl_socket to None

    try:
        # Create an SSL context
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certfile='server.crt', keyfile='key.pem')

        # Wrap the client socket with SSL/TLS
        ssl_socket = ssl_context.wrap_socket(client_socket, server_side=True)

        # Ask client for a nickname
        ssl_socket.send("Enter your nickname: ".encode('utf-8'))
        nickname = ssl_socket.recv(1024).decode('utf-8')
        clients[ssl_socket] = nickname

        # Welcome message to the new client
        ssl_socket.send(f"Welcome, {nickname}! Type 'quit' to exit.\n".encode('utf-8'))

        # Notify other clients about the new connection
        broadcast(f"{nickname} has joined the chat.", nickname)

        # Creating a decrypting function for decrypting the message from the client
        def decrypt(key, associated_data, iv, ciphertext, tag):
            decryptor = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend()).decryptor()

            decryptor.authenticate_additional_data(associated_data)

            return decryptor.update(ciphertext) + decryptor.finalize()


        #Set the key for the encrypting/decrypting as well as associated data which helps with authentication
        key = codecs.decode('36f12345be4dbd22f050515c73fcf7c3', 'hex_codec')
        associated_data = b'Extra data to add for messages'

        # Continuously receive and broadcast messages
        while True:
            ciphertext = ssl_socket.recv(1024).decode()
            iv, ciphertext, tag = map(codecs.decode, ciphertext.split('|'), ['hex_codec'] * 3)

            plaintext = decrypt(key, associated_data, iv, ciphertext, tag).decode()
            print(f'Plaintext: {plaintext}')

            if plaintext.lower() == 'quit':
                break
            # Display the nickname of the client who sent the message on the server
            print(f"{nickname}: {plaintext}")

            # Broadcast the message to other clients
            broadcast(plaintext, nickname)

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        if ssl_socket is not None:
            remove_client(ssl_socket)

# Function to remove a client from the dictionary and broadcast their exit
def remove_client(client_socket):
    if client_socket in clients:
        nickname = clients[client_socket]
        print(f"{nickname} has left the chat.")
        del clients[client_socket]
        client_socket.close()

        # Handles any issues that my rise when sending the left the chat messages to the other clients connected.
        for other_client_socket in list(clients.keys()):
            try:
                other_client_socket.send(f"{nickname} has left the chat.".encode('utf-8'))
            except:
                pass

# Create a socket for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_host = 'localhost'
server_port = 12007

# Bind the server socket to the host and port
server_socket.bind((server_host, server_port))

# Listen for incoming connections
server_socket.listen()

print(f"Server listening on {server_host}:{server_port}")

# Accept and handle incoming connections
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    # Create a new thread for each client
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()


