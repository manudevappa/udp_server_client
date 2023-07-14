import socket

# Server information
server_ip = '192.168.0.136'  # Replace with the server IP address
server_port = 12345  # Replace with the server port number

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    # Get user input
    message = input("Enter a message to send (or 'q' to quit): ")

    if message.lower() == 'q':
        break

    # Send the message to the server
    client_socket.sendto(message.encode(), (server_ip, server_port))

    # Receive a response from the server
    response, server_address = client_socket.recvfrom(1024)
    print("Received response: ", response.decode())

# Close the socket
client_socket.close()