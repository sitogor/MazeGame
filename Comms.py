import socket

# TCP_IP = '137.222.95.220'
# TCP_IP = '192.168.1.1'
TCP_IP = '169.254.11.250'
TCP_PORT = 5005
BUFFER_SIZE = 20
MESSAGE = "Hello, World!"

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE.encode())
data = s.recv(BUFFER_SIZE)
s.close()
print("received data:", data)
