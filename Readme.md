# UDP Chat App

Note: This code only works on Linux systems. If you are using Windows, you can use Cygwin or WSL.

### What is this?

This is a terminal chat app based on urwid, UDP socket, built for fun.

### Prerequisites

1. Install Python 3.xx.
2. Install urwid: `pip install urwid`

## How to run?

There are two scripts:

1. Server
2. Client

### What does the server code do?

- Maintains a connected client list.
- Sends/receives messages to/from clients.
- Broadcasts messages.
- Adds/removes clients from the channel.

#### How to set up the server?

Run the following command:

```
python3 server.py
```

- Take note of the IP address (provide it to clients for connection).

### What does the client code do?

- Joins/quits the chatroom.
- Sends/receives messages in the group.

#### How to set up the client?

Run the following command:

```
python3 udp_client.py
```

#### Supportive Commands

| Command            | Description                                        |
| ------------------ | -------------------------------------------------- |
| /ip <ip_address>   | Connect to the server. Enter the server IP address. |
| /join <user_name>  | Enter your name to display in the group chat.      |
| /q or /quit        | Quit or exit a group chat.                         |

### How to start?

1. Ensure all clients are connected to the same network.
2. Start the server first (`python3 server.py`).
3. On the client side, run the code (`python3 udp_client.py`).
4. Provide the server's IP address to the client.
   Example: `/ip 192.168.0.130`
5. Join the chat room.
   Example: `/join manu`
6. Send messages and have fun.

Sample screen:


![image](https://github.com/manudevappa/udp_server_client/assets/30531874/b650a570-af08-4db4-84ec-14e2a7b43978)
