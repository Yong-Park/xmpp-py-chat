"""
Universidad del Valle de Guatemala
(CC3067) Redes
Santiago Taracena Puga (20017)
"""

# Required libraries.
import os
import ssl
import socket
from dotenv import load_dotenv

# Required modules.
from utils.send_message import send_message
from utils.receive_message import receive_message
from utils.build_auth_message import build_auth_message
from utils.build_presence_message import build_presence_message
from utils.build_chat_message import build_chat_message

# Function that loads .env files into the project.
load_dotenv(".env")

# XMPP server basic configuration.
XMPP_SERVER = os.getenv("XMPP_PY_CHAT_SERVER")
XMPP_PORT = os.getenv("XMPP_PY_CHAT_PORT")

# Session details input.
jid = input("Input your JID: ")
password = input("Input your password: ")

# Instance of SSL context to connect.
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

# Additional security options.
context.options |= ssl.OP_NO_SSLv2
context.options |= ssl.OP_NO_SSLv3

# XMPP server connection with a socket.
xmpp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
xmpp_socket = context.wrap_socket(xmpp_socket, server_hostname=XMPP_SERVER)

# Actual socket connection.
xmpp_socket.connect((XMPP_SERVER, int(XMPP_PORT)))

# Session started message.
auth_message = build_auth_message(jid, password)
send_message(xmpp_socket, auth_message)

# Receive and show the server's response.
response = receive_message(xmpp_socket)
print(f"Server response: {response}")

# Send a pressence message.
presence_message = build_presence_message()
send_message(xmpp_socket, presence_message)

# Client's main loop.
while (True):

    # Read destination JID and message body.
    to_jid = input("To (JID): ")
    body = input("Message: ")

    # Build and send the message.
    chat_message = build_chat_message(to_jid, body)
    send_message(xmpp_socket, chat_message)

    # Receive and show the server's response.
    response = receive_message(xmpp_socket)
    print(f"Server response: {response}")

# Function that closes the socket.
xmpp_socket.close()
