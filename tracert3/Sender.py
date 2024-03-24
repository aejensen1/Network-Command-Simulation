import socket
import time
import random

# Constants
serverName = '127.0.0.1'
serverPort = 12000
num_requests = 4
timeout = 5
ttl_limit = 7

# Initialize the routing table with an empty list
routing_table = []

# Generate a random ID for the destination
dest_id = f"Router {random.randint(1, 100)}"

print(f"Pinging {dest_id} with {num_requests} packets:")

# Create a socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for ttl in range(1, ttl_limit + 1):
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
            
            # Extract router IP from serverAddress
            router_ip = ".".join(map(str, serverAddress[0].split('.')[-3:]))
            print(f"Reply from {router_ip}: bytes={len(modifiedMessage)} time={rtt:.0f}ms TTL={ttl}")
            packets_received += 1

            # Add the router IP to the routing table if it's not already present
            if router_ip not in routing_table:
                routing_table.append(router_ip)
        except socket.timeout:
            print("Request timed out")
            break  # Exit the loop if timeout occurs

        packets_sent += 1

    # Exit the loop if at least one packet is received
    if packets_received > 0:
        break

# Close the socket
clientSocket.close()

# Print the routing table
print("\nRouting Table:")
for i, address in enumerate(routing_table):
    print(f"{i+1}. {address}")
