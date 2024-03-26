# Sender

# Improved Sender (Client) Script

import socket
import time
import random

serverName = '127.0.0.1'
all_routers = list(range(12000, 12016)) # same as in Receiver script
dest_id = random.choice(all_routers) # Destination is a random router

print(f"Traceroute to ({serverName}:{dest_id}), 30 hops max, 60 byte packets")

# Create a socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for ttl in range(1, 31): # max 30 (ttl_limit)
    clientSocket.settimeout(5)
    message = f"{ttl},{dest_id}"
    initial_router = random.choice(all_routers) # Choose initial router randomly
    clientSocket.sendto(message.encode(), (serverName, initial_router))

    try:
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        router_port, timestamp = (float(i) if '.' in i else int(i) for i in modifiedMessage.decode().split(','))
        delay = (time.time() - timestamp) * 1000  # Convert to milliseconds
        print(f"{ttl:<2} router port - {router_port}  {delay:.3f} ms")

        # Break if reached the destination
        if router_port == dest_id:
            break

    except socket.timeout:
        print(f"{ttl:<2} * Timeout | switching routers")
        all_routers.remove(initial_router) # remove previous router from available choices
        if not all_routers: # if there are no more routers to switch to
            print("All routers lead to timeout. Exiting...")
            break

# Close the socket
clientSocket.close()
