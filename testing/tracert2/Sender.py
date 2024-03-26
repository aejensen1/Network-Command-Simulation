import socket
import time
import random

serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

num_requests = 4
timeout = 5  # 5 seconds timeout
max_hops = 8  # Maximum number of hops
ttl_limit = 7  # Maximum TTL value

# Initialize the routing table with an empty list
routing_table = []

# Generate a random ID for the destination
dest_id = f"Router {random.randint(1, 100)}"

print(f"Pinging {dest_id} with {num_requests} packets:")

for ttl in range(1, ttl_limit + 1):  # Iterate over TTL values
    clientSocket.settimeout(timeout)  # Set socket timeout

    # Reset counters and lists for each TTL value
    packets_sent = 0
    packets_received = 0

    for i in range(num_requests):
        message = f"{ttl},{dest_id}"  # Include TTL and destination ID in the message
        start_time = time.time()
        clientSocket.sendto(message.encode(), (serverName, serverPort))

        try:
            modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
            end_time = time.time()
            rtt = (end_time - start_time) * 1000  # Convert to milliseconds
            print(f"Reply from {serverAddress[0]}: bytes={len(modifiedMessage)} time={rtt:.0f}ms TTL={ttl}")
            packets_received += 1

            # Add the router IP to the routing table if it's not already present
            if serverAddress[0] not in routing_table:
                routing_table.append(serverAddress[0])
        except socket.timeout:
            print("Request timed out")
            break  # Exit the loop if timeout occurs

        packets_sent += 1

    # Exit the loop if at least one packet is received
    if packets_received > 0:
        break

clientSocket.close()
