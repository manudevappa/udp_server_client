import socket

# Server information
server_ip = '192.168.238.221'  # Replace with the server IP address
server_port = 12345  # Replace with the server port number

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client_socket.setblocking(0)

while True:
    print("start")
    try:
        response, server_address = client_socket.recvfrom(1024)
    except socket.error:
        pass
    else: 
        print("Received response: ", response.decode())
    print("complte")    

    # Get user input
    message = input("Enter a message to send (or 'q' to quit): ")

    if message.lower() == 'q':
        break

    # Send the message to the server
    client_socket.sendto(message.encode(), (server_ip, server_port))

    
# Close the socket
client_socket.close()