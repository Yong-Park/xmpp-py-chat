"""
Universidad del Valle de Guatemala
(CC3067) Redes
Santiago Taracena Puga (20017)
"""

# Required XML library.
import xml.etree.ElementTree as ET

# Function that builds a started session XMPP message.
def build_auth_message(jid, password):
    auth = ET.Element("auth", {"mechanism": "PLAIN"})
    auth.text = "\x00" + jid + "\x00" + password
    message = ET.Element("message")
    message.append(auth)
    return ET.tostring(message)
