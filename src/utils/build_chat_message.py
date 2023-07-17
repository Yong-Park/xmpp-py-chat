"""
Universidad del Valle de Guatemala
(CC3067) Redes
Santiago Taracena Puga (20017)
"""

# Required XML library.
import xml.etree.ElementTree as ET

# Function that builds a XMPP chat message.
def build_chat_message(to_jid, body):
    message = ET.Element('message', {'type': 'chat', 'to': to_jid})
    message_body = ET.SubElement(message, 'body')
    message_body.text = body
    return ET.tostring(message)
