from socket import *
import time

serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

num_requests = 4
timeout = 1  # 1 second timeout

packets_sent = 0
packets_received = 0
rtt_values = []

print(f"Pinging {serverName} with {num_requests} packets:")

for i in range(num_requests):
    message = f"Packet {i+1}"  # Predetermined content in the packets
    start_time = time.time()
    clientSocket.sendto(message.encode(), (serverName, serverPort))

    clientSocket.settimeout(timeout)
    try:
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        end_time = time.time()
        rtt = (end_time - start_time) * 1000  # Convert to milliseconds
        print(f"Reply from {serverName}: bytes={len(modifiedMessage)} time={rtt:.0f}ms TTL=55")
        rtt_values.append(rtt)
        packets_received += 1
    except TimeoutError:
        print("Request timed out")
        pass
        #print(f"Request timed out: {e}")
        #packets_lost += 1  # Count timeout as a lost packet
        #continue

    packets_sent += 1

clientSocket.close()

# Calculate statistics
packets_lost = packets_sent - packets_received
loss_percentage = (packets_lost / packets_sent) * 100 if packets_sent > 0 else 0
min_rtt = min(rtt_values) if rtt_values else 0
max_rtt = max(rtt_values) if rtt_values else 0
avg_rtt = sum(rtt_values) / len(rtt_values) if rtt_values else 0

print(f"\nPing statistics for {serverName}:")
print(f"    Packets: Sent = {packets_sent}, Received = {packets_received}, Lost = {packets_lost} ({loss_percentage:.0f}% loss),")
print("Approximate round trip times in milli-seconds:")
print(f"    Minimum = {min_rtt:.0f}ms, Maximum = {max_rtt:.0f}ms, Average = {avg_rtt:.0f}ms")

