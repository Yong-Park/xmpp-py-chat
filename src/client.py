"""
Universidad del Valle de Guatemala
(CC3067) Redes
Santiago Taracena Puga (20017)
Proyecto 1 - Protocolo XMPP
"""

import slixmpp
from slixmpp.exceptions import IqError, IqTimeout

class Client(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid=jid, password=password)

    async def start(self):
        pass
