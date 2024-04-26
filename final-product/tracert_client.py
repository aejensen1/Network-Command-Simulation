from socket import *
import time

serverName = '127.0.0.1'  # Assuming server is running on localhost
serverPorts = [12000, 12001, 12002, 12003, 12004, 12005, 12006, 12007, 12008, 12009]  # Ports the server is listening on
timeout = .5  # 1 second timeout
num_pings = 3 # Number of pings per hop

max_hops = len(serverPorts)  # Maximum number of hops

print(f"Tracing route to {serverName}")
print(f"over a maximum of {max_hops} hops:\n")

for i, port in enumerate(serverPorts, start=1):
    print(f" {i} ", end='')  # Print hop number

    rtt_values = []  # List to store RTT for each ping

    for _ in range(num_pings):
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        clientSocket.bind(('', 0))  # Bind to any available local port
        start_time = time.time()
        clientSocket.sendto(b"", (serverName, port))  # Send an empty packet to the server
        clientSocket.settimeout(timeout)
        try:
            modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
            end_time = time.time()
            rtt = (end_time - start_time) * 1000  # Convert to milliseconds
            print(f"  {rtt:.0f} ms ", end='')  # Print RTT
            #rtt_values.append(rtt)
        except TimeoutError:
            print(" * ", end='')  # Print "*" for timeout
        clientSocket.close()

    #if rtt_values:
        # avg_rtt = sum(rtt_values) / len(rtt_values)
    print(f"  {serverName} [{port}]")

print("\nTrace complete.")

