# Sender

import socket
import time

num = 0

def send_ping(host, port):
    global num  # Declare 'num' as global to modify it inside the function
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(6)  # Set timeout to 6 seconds
        start_time = time.time()
        try:
            s.sendto(b"Ping", (host, port))
            data, addr = s.recvfrom(1024)
            end_time = time.time()
            num += 1  # Increment 'num'
            print(f"{num}  (Time: {int((end_time - start_time) * 1000)} ms)  {addr}")
        except socket.timeout:
            print("*** Timeout occurred while waiting for response from {addr}. Resending ping...")
            send_ping(host, port)  # Resend the ping

def main():
    host = 'localhost'  # Change this to your destination host
    ports = [10000, 10001, 10002, 10003]  # Four ports to simulate routers and destination
    destination_port = ports[-1]
    print(f"Sending pings to {host} (Destination port: {destination_port})")
    for port in ports:
        send_ping(host, port)
        time.sleep(1)  # Adjust delay between pings if necessary

if __name__ == "__main__":
    main()

