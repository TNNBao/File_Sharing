import os 
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))

file = open(r"D:/CODE/Python_project/File_Sharing/assets/images/auth.png", "rb")
file_size = os.path.getsize(r"D:/CODE/Python_project/File_Sharing/assets/images/auth.png")

client.send("received file".encode())
client.send(str(file_size).encode())

data = file.read()
client.sendall(data)
client.send(b"<END>")

file.close()
client.close()