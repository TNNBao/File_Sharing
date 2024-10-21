import socket
import tqdm

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()

client, addr = server.accept()

fname = client.recv(1024).decode()
print(fname)
fsize = client.recv(1024).decode()
print(fsize)