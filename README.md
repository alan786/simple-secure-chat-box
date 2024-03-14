# Simple Secure Chat Server
This is a simple secure chat server implemented in Python, utilizing SSL/TLS encryption and AES-GCM message encryption for secure communication between clients and the server.

## Prerequisites
Before running the code, ensure you have the following installed:

- Python 3: Make sure you have Python 3 installed on your system. You can download it from the official Python website.

- Python Cryptography Library: This code uses the cryptography library for encryption and decryption. Install it using pip:pip install cryptography

## Getting Started
- Download the Code: Clone or download the code from the repository.

- Running the Server:
    - Open a terminal or command prompt.

    - Navigate to the directory containing the code.

- Run the server script: python server.py

    - Running the Client: Open another terminal or command prompt.

    - Navigate to the directory containing the code.

    - Run the client script: python client.py
- Usage:

    - When the client is launched, it will prompt you to enter a nickname.
    - Type a nickname and press Enter.
    - You can now send messages to other connected clients.
    - Type "quit" to exit the chat.

## Additional Notes
- Make sure the server.py script is running before launching any clients.
- If you encounter any issues, check your SSL/TLS certificate files and ensure they are correctly configured.
- This is a basic implementation and may lack certain features or robustness required for production use. Use it for educational purposes or extend it to suit your needs.