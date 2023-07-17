"""
Universidad del Valle de Guatemala
(CC3067) Redes
Santiago Taracena Puga (20017)
"""

# Required XML library.
import xml.etree.ElementTree as ET

# Function that builds a presence XMPP message.
def build_presence_message():
    presence = ET.Element("presence")
    message = ET.Element("message")
    message.append(presence)
    return ET.tostring(message)
