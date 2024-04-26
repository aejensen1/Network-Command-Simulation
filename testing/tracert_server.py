from socket import *
import random
import time

# Define a list of 10 port numbers the server will listen on
serverPorts = [12000, 12001, 12002, 12003, 12004, 12005, 12006, 12007, 12008, 12009]

# Create sockets and bind them to the corresponding ports
serverSockets = [socket(AF_INET, SOCK_DGRAM) for _ in serverPorts]
for i, port in enumerate(serverPorts):
    serverSockets[i].bind(('', port))

print("The server is ready to receive")

while True:
    for serverSocket in serverSockets:
        message, clientAddress = serverSocket.recvfrom(2048)
        # Simulate unreliable behavior by randomly choosing not to reply
        if random.random() < .9:  # 80% chance of replying
            modifiedMessage = message.decode().upper()
            # Simulate variable RTT by waiting for a random period
            time.sleep(random.uniform(0.1, 0.5))  # Wait between 100ms to 500ms
            serverSocket.sendto(modifiedMessage.encode(), clientAddress)
        else:
            print(f"Packet dropped on port {serverSocket.getsockname()[1]} (unreliable behavior)")

