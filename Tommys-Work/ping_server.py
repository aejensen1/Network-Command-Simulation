from socket import *
import random
import time

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("The server is ready to receive")

while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    # Simulate unreliable behavior by randomly choosing not to reply
    if random.random() < 0.8:  # 80% chance of replying
        modifiedMessage = message.decode().upper()
        # Simulate variable RTT by waiting for a random period
        time.sleep(random.uniform(0.1, 0.5))  # Wait between 100ms to 500ms
        serverSocket.sendto(modifiedMessage.encode(), clientAddress)

