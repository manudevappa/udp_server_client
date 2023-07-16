import socket
import json

# Server information
server_ip = ''  # Replace with the server IP address
server_port = 12345  # Replace with the desired server port number

# Array to store address and name of the client
rows = 100
cols = 100
client_list = [[0] * cols for _ in range(rows)]

# Temporary username
temp_username = None
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

print("Server is running in ", server_ip)

# Dictionary to store client addresses
class Device:
    def __init__(self, ip_address, port, name, connection_status):
        self.ip_address = ip_address
        self.port 		= port 
        self.name 		= name
        self.connection_status = connection_status
    
    def update_existing_ip(self, port, name, connection_status):
        self.port 			= port
        self.name 			= name
        self.connection_status = connection_status

    def update_connection_status(self, update_port):
	    self.connection_status = update_port

# Function to add a new device
def add_device(ip_address, port, name, connection_status):
	# Check if the IP is already connected
    for client in client_list:
    	if client.ip_address == ip_address:
    		client.update_existing_ip(port, name, connection_status)
    		return()
    new_device = Device(ip_address, port, name, connection_status)
    client_list.append(new_device)	

# Encode JSON 
def json_encode(towhome, message_type, uname, message):
	# Create a dictionary
	data = {
		'to_whom' 	: towhome,
	    'type'		: message_type,
	    'u_name' 	: uname,
	    'message' 	: message
	}
    # Convert the dictionary to a JSON string	
	json_data = json.dumps(data)
	# Return the JSON object
	return json_data

# Initialize an empty list
client_list = []


def ack_send(client_address, message_type, message, u_name):
	for client in client_list:
		print("search", client.ip_address)
		if client.ip_address != client_address[0]:
			if client.connection_status == True:
				encoded_data = json_encode("group", message_type, u_name, message)
				print("group send ", encoded_data)
				client_addr = client.ip_address, client.port
				server_socket.sendto(encoded_data.encode(), client_addr)

#  Prepare socket and send group message
def group_send(client_address, message_type, message, u_name):
	for client in client_list:
		print("search", client.ip_address)
		if client.ip_address != client_address[0]:
			if client.connection_status == True:
				encoded_data = json_encode("group", message_type, u_name, message)
				# print("group send ", encoded_data)
				client_addr = client.ip_address, client.port
				server_socket.sendto(encoded_data.encode(), client_addr)


def send_socket(client_address, message, event, u_name):
	match event:
		case "join":
			encoded_data = json_encode("self", "join_ack", None, message)
			server_socket.sendto(encoded_data.encode(), client_address)
			ack_send(client_address, "new_joinee", None, u_name)

		case "quit":
			encoded_data = json_encode("self", "quit_ack", None, " ")
			server_socket.sendto(encoded_data.encode(), client_address)
			ack_send(client_address, "someone_left", None, u_name)
		   
		case "group_chat":
			group_send(client_address, "group", message, u_name)


while True:
	# Receive a message from a client
	byte_message, client_address = server_socket.recvfrom(1024)
	message = byte_message.decode()
	print("From ",client_address[0], message)
	json_data = json.loads(message)
	message_type = json_data["type"] 
	match message_type:
		case "join":
			# Add the client to the client_addresses dictionary
			get_ip_address	= client_address[0] 
			get_port		= client_address[1]
			get_username	= json_data['u_name']
			get_satus 		= True
			add_device(get_ip_address, get_port, get_username, get_satus)
			# Send req accept message to client
			send_socket(client_address, "", "join", json_data['u_name'])

		case "quit":
			for client in client_list:
				if client.ip_address == client_address[0]:
					send_socket(client_address, "", "quit")
					client.update_connection_status(False)
					break
		case "group":
			send_socket(client_address, json_data['message'], "group_chat", json_data['u_name'])
		
