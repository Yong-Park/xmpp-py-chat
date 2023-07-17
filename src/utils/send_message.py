"""
Universidad del Valle de Guatemala
(CC3067) Redes
Santiago Taracena Puga (20017)
"""

# Function that sends a XMPP message to the server.
def send_message(socket, message):
    socket.send(message.encode())
