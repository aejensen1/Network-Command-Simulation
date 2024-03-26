import socket
import time
import random

serverPort = 12000

# Simulated router IDs (fake port numbers)
router_ports = [12001, 12002, 12003, 12004, 12005, 12006, 12007, 12008, 12009, 12010]

# Create a socket for each router
serverSockets = []
for port in router_ports:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind(('127.0.0.1', port))
    serverSockets.append(serverSocket)

print("Receivers are ready to receive")

while True:
    for serverSocket in serverSockets:
        message, clientAddress = serverSocket.recvfrom(1024)
        ttl, dest_id = message.decode().split(',')
        ttl = int(ttl)
        
        # Check if TTL has expired
        if ttl <= 0:
            print("Packet dropped (TTL expired)")
            continue

        # Simulate forwarding to a random router
        next_port = random.choice(router_ports)
        forward_message = f"{ttl - 1},{dest_id}"
        serverSocket.sendto(forward_message.encode(), ('127.0.0.1', next_port))
        print(f"Packet forwarded to port {next_port}")

        # Send back the router port number to the sender
        serverSocket.sendto(str(serverSocket.getsockname()[1]).encode(), clientAddress)

for serverSocket in serverSockets:
    serverSocket.close()
