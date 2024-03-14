# Importing functions for the server programming
import socket
import ssl
import threading

# Importing functions for encryption/decryption through Python's cryptography functions
import codecs
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Function to handle receiving messages from the server
def receive_messages():
    while True:
        try:
            message = ssl_socket.recv(1024).decode()
            print(message)
        except:
            print("Connection to the server has been lost.")
            break

# Create a socket for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Create an SSL context
ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile='server.crt')

# Wrap the client socket with SSL/TLS
ssl_socket = ssl_context.wrap_socket(client_socket, server_hostname='localhost')

# Connect to the server
server_host = 'localhost'
server_port = 12007
ssl_socket.connect((server_host, server_port))

# Ask the user for a nickname
nickname = input("Enter your nickname: ")
ssl_socket.send(nickname.encode('utf-8'))

# Start a thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

def encrypt(key, plaintext, associated_data):
    iv = os.urandom(12)
    encryptor = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend()).encryptor()
    encryptor.authenticate_additional_data(associated_data)
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return iv, ciphertext, encryptor.tag


# Set the key for the encrypting/decrypting as well as associated data which helps with authentication
key = codecs.decode('36f12345be4dbd22f050515c73fcf7c3', 'hex_codec')
associated_data = b'Extra data to add for messages'

# Continuously send messages to the server
while True:
    message = input()
    plaintext = message.encode('utf-8')
    iv, ciphertext, tag = encrypt(key, plaintext, associated_data)
    print(f'Ciphertext: {ciphertext}')
    message_to_send = f"{iv.hex()}|{ciphertext.hex()}|{tag.hex()}"
    ssl_socket.send(message_to_send.encode())
    if message.lower() == 'quit':
        break


# Close the socket when the client exits
ssl_socket.close()




