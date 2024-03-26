# Sender

import socket
import time
import random

serverName = '127.0.0.1'
ttl_limit = 30  # Maximum TTL to trace route
all_routers = list(range(12000, 12016))  # same as in Receiver script
dest_id = 12015  # Destination is always the host

# Create a socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Traceroute to ({serverName}:{dest_id}), {ttl_limit} hops max, 60 byte packets")

for ttl in range(1, ttl_limit):
    clientSocket.settimeout(5)  # Set socket timeout
    message = f"{ttl},{dest_id}"
    # Choose initial router randomly; notice we keep it out of the loop so it's not redefined in case of a timeout
    initial_router = random.choice(all_routers)

    try:
        clientSocket.sendto(message.encode(), (serverName, initial_router))
        print(f"Packet sent to router {initial_router} with ttl={ttl}")  # log which router was used

        while True:  # keep receiving until timeout
            modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
            router_port, timestamp = (float(i) if '.' in i else int(i) for i in modifiedMessage.decode().split(','))
            delay = (time.time() - timestamp) * 1000  # Convert to milliseconds
            print(f"{ttl:<2} router port - {router_port}  {delay:.3f} ms")

            # Break if reached the destination
            if router_port == dest_id:
                break

    except socket.timeout:
        print(f"{ttl:<2} *")
        if ttl == ttl_limit - 1:
            print("Ending Traceroute due to max TTL")
            break  # Exit loop if max TTL is reached

clientSocket.close()  # Close the socket
