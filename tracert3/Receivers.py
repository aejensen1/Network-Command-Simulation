# Receiver

# Improved Receiver (Router) Script

import socket
import time
import random

# List of all router port numbers
all_routers = list(range(12000, 12016))  # 16 ports from 12000 to 12015

# Initialize the routing table with static entries for next_hop
routing_table = {i: all_routers[(all_routers.index(i) + 1) % len(all_routers)]
                 for i in all_routers}

def main():
    print("Router is running")

    # Each router binds its own port
    for serverPort in all_routers:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverSocket.bind(('127.0.0.1', serverPort))

        while True:
            message, clientAddress = serverSocket.recvfrom(1024)
            ttl, dest_id = (int(i) for i in message.decode().split(','))

            # Check if TTL has expired
            if ttl <= 0:
                print(f"Packet from {clientAddress[1]} dropped (TTL expired)")
                continue

            # If packet should be dropped
            if random.random() >= 0.95:  # 5% drop rate
                print(f"Packet from {clientAddress[1]} dropped (Packet loss)")
                continue

            # If we are the last hop or the destination, send answer back to sender
            if ttl == 1 or serverPort == dest_id:
                answer = f"{serverPort},{time.time()}"
                serverSocket.sendto(answer.encode(), clientAddress)
                print(f"Answered to sender from port {clientAddress[1]}")
            else:  
                print(f"Packet from {clientAddress[1]} forwarded (TTL={ttl - 1})")
                next_router = routing_table[serverPort] # Choose next router based on routing table
                time.sleep(0.1)  # delay before sending to next router
                serverSocket.sendto(message.encode(), ('127.0.0.1', next_router))

        serverSocket.close()

if __name__ == "__main__":
    main()
