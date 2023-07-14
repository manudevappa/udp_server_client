import socket

# Server information
server_ip = '192.168.0.136'  # Replace with the server IP address
server_port = 12345  # Replace with the desired server port number

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_ip, server_port))

# Dictionary to store client addresses
client_addresses = {}

print("Server is running...")

while True:
    # Receive a message from a client
    message, client_address = server_socket.recvfrom(1024)
    message = message.decode()
    print(message)
    if message.startswith("/join "):
        # Add the client to the client_addresses dictionary
        username = message[6:]
        client_addresses[username] = client_address
        print(f"Client '{username}' joined the chat.")

    elif message.startswith("/quit"):
        # Remove the client from the client_addresses dictionary
        for username, address in client_addresses.items():
            if address == client_address:
                del client_addresses[username]
                print(f"Client '{username}' left the chat.")
                break

    else:
        # Relay the message to all other clients
        for username, address in client_addresses.items():
            if address != client_address:
                relay_message = f"{username}: {message}"
                server_socket.sendto(relay_message.encode(), address)
                print(f"Relaying message from '{username}' to other clients.")