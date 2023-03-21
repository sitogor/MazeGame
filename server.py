import socket
TCP_IP = '169.254.22.20'
TCP_PORT = 5005
BUFFER_SIZE = 20

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
conn,addr = s.accept()
print('Connection adddress:', addr)
while 1:
	data= conn.recv(BUFFER_SIZE)
	if not data:break
	print("recieved data:", data)
	#conn.send(data)
conn.close()
