"""
Universidad del Valle de Guatemala
(CC3067) Redes
Santiago Taracena Puga (20017)
"""

# Function that receives a XMPP message from the server.
def receive_message(socket):
    data = socket.recv(4096)
    return data.decode()
