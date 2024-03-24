import socket
import time
import random

# Constants
serverPort = 12000
ttl_limit = 7

# Initialize the routing table with an empty list
routing_table = []

def forward_packet(ttl, dest_id):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind(('127.0.0.1', serverPort))
    forward_message = f"{ttl - 1},{dest_id}"
    serverSocket.sendto(forward_message.encode(), ('127.0.0.1', serverPort))
    serverSocket.close()

def main():
    print("Receiver is ready to receive")

    while True:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverSocket.bind(('127.0.0.1', serverPort))
        message, clientAddress = serverSocket.recvfrom(1024)
        ttl, dest_id = message.decode().split(',')
        ttl = int(ttl)
        serverSocket.close()

        # Check if TTL has expired
        if ttl <= 0:
            print("Packet dropped (TTL expired)")
            continue

        # Simulate forwarding to a random router
        forward_packet(ttl, dest_id)
        print(f"Packet forwarded to a random router")

        # Send back the router port number to the sender
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverSocket.bind(('127.0.0.1', serverPort))
        serverSocket.sendto(str(serverPort).encode(), clientAddress)
        serverSocket.close()

        # Record the sender's IP address in the routing table
        if clientAddress[0] not in routing_table:
            routing_table.append(clientAddress[0])

        # Exit the loop if the routing table has reached its limit
        if len(routing_table) >= ttl_limit:
            break

if __name__ == "__main__":
    main()
