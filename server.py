import socket

# Server information
server_ip = ''  # Replace with the server IP address
server_port = 12345  # Replace with the desired server port number

# Create a UDP socket
get_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # doesn't even have to be reachable
    get_ip.connect(('192.255.255.255', 1))
    server_ip = get_ip.getsockname()[0]
except:
    server_ip = '127.0.0.1'

get_ip.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_ip, server_port))

# Dictionary to store client addresses
client_addresses = {}

print("Server is running in ", server_ip)

while True:
    # Receive a message from a client
    message, client_address = server_socket.recvfrom(1024)
    message = message.decode()
    print(message)
    if message.startswith("/join "):
        # Add the client to the client_addresses dictionary
        username = message[6:]
        client_addresses[username] = client_address
        print(f"Client '{username}' joined the chat.", client_address)
        text = "jAcptD"
        server_socket.sendto(text.encode(), client_address)

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
                print("message", relay_message)
                print(f"Relaying message from '{client_address}' to other clients.")