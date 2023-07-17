# UDP Chat APP 

Note: This code only works in Linux System. You can use Cygwin, WSL if you are using Windows

### What is this ?
    urwid based terminal chat app, build for fun. 

### Preacquisition!
1. Install Python3.xx
2. Instal urwid <pip install urwid>

## How to run ?
    There are two scripts:
    1. Server
    2. Client

### What does server code do ?
- Maintain connected client list
- Send/Receive messages from/to client
- Broadcast Message
- Add/Remove client from channel
#### How to setup Server ?
    python3 server.py
- Run above command
- Note down the IP address (give that to clients to connect)


### What does client code do ?
- Join/Quit chatroom
- Send/Receive messages in group

#### How to setup Client ?
    python3 udp_client.py
#### Supportive Commands
| Command | Description |
| ------ | ------ |
| /ip <ip_address> | Connect to server. Enter Server IP |
| /join <user_name> | Enter you name to display in group chat |
| /q or /quit | Quit or exit a group chat |

### How to start ?
    1. Make sure all clients connected in a same network
    2. Start Server first (python3 server.py)
    3. In Client side, start run code (python3 udp_client.py)
    4. Provide Server IP address to cient 
        Ex:    /ip 192.168.0.130
    5. Join chat room
        Ex:     /join manu
    6. Send messages, Have Fun.

