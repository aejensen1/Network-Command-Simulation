# Receiver

import socket
import time
import random
import threading

# Constants
all_routers = list(range(12000, 12016)) 
dest_host = random.choice(all_routers) # Destination as random router
all_routers.remove(dest_host)
packet_drop_rate = 5 # 5% 

def start_router(serverPort):
    # Create a router socket
    routerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    routerSocket.bind(('localhost', serverPort))
    print(f"Router {serverPort} is ready to receive")

    while True:
        message, clientAddress = routerSocket.recvfrom(1024)
        ttl, dest_id = list(map(int, message.decode().split(',')))

        if ttl <= 0:
            was_dropped=False
            answer = f"{serverPort},{time.time()}"
            print(f"Router {serverPort} returning message to Sender: {clientAddress[1]}") # add this line
            if serverPort == dest_host:
                routerSocket.sendto(answer.encode(), clientAddress)
                msg = "Destination reached"
            else:
                routerSocket.sendto(answer.encode(), clientAddress)
                msg = "due to TTL expired"
            print(f"Router {serverPort} replied to {clientAddress[1]} {msg}")
            routerSocket.close()

        elif ttl > 0:
            next_hop = all_routers[(all_routers.index(serverPort) + 1) % len(all_routers)]
            if random.randint(1, 100) > packet_drop_rate:  # 95% chance packet will succeed
                forward_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                forward_socket.sendto(message, ('localhost', next_hop))
                forward_socket.close()
                print(f"Router {serverPort} forwarded packet from {clientAddress[1]} to {next_hop} TTL={ttl}")
            else:  # 5% chance of packet drop
                was_dropped=True
                print(f"Packet from {clientAddress[1]} dropped by {serverPort} due to packet loss")


if __name__ == "__main__":
    threads = []
    for routerPort in all_routers:
        thread = threading.Thread(target=start_router, name=f"Router-{routerPort}", args=(routerPort,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
