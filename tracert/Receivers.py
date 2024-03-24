from socket import *
import random
import time

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('127.0.0.1', serverPort))

# List to store known router IDs
known_router_ids = []

print("Receiver is ready to receive")

while True:
    message, clientAddress = serverSocket.recvfrom(1024)
    ttl, dest_id = message.decode().split(',')
    ttl = int(ttl)
    
    # Simulate TTL decrement
    ttl -= 1
    
    # Add the sender's ID to the list of known router IDs
    sender_id = clientAddress[0]
    if sender_id not in known_router_ids:
        known_router_ids.append(sender_id)
    
    # If TTL is positive, forward the packet to a random router
    if ttl > 0:
        # Choose a random router ID from the known router IDs list
        next_id = random.choice(known_router_ids)
        
        # If the next router ID is the destination, send a response back to the sender
        if next_id == dest_id:
            response_message = f"{ttl},{next_id}"
            serverSocket.sendto(response_message.encode(), clientAddress)
            print(f"Packet forwarded to destination ({dest_id})")
        else:
            # Otherwise, forward the packet to the randomly chosen router ID
            forward_message = f"{ttl},{dest_id}"
            serverSocket.sendto(forward_message.encode(), (next_id, serverPort))
            print(f"Packet forwarded to {next_id}")

    # If TTL reaches 0, drop the packet
    else:
        print("Packet dropped (TTL expired)")

serverSocket.close()
