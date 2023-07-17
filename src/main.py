import socket

project_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
project_socket.connect(("alumchat.xyz", 8080))
