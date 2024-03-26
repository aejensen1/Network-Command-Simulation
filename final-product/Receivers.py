# Receivers

import socket
import random
import time

def receive_ping(port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('localhost', port))
        print(f"Router on port {port} is ready to receive pings...")
        success_response_sent = False
        while not success_response_sent:
            data, addr = s.recvfrom(1024)
            if random.random() < 0.8:  # Hit rate. Adjust the probability as needed
                print(f"Received ping from {addr} on port {port}")
                s.sendto(b"Success", addr)
                success_response_sent = True  # Set flag to True to indicate successful response
            else:
                print(f"No response sent to ping from {addr} on port {port}")

def main():
    ports = [10000, 10001, 10002, 10003]  # Four ports to simulate routers and destination
    for port in ports:
        receive_ping(port)

if __name__ == "__main__":
    main()

