"""
Universidad del Valle de Guatemala
(CC3067) Redes
Santiago Taracena Puga (20017)
Proyecto 1 - Protocolo XMPP
"""

import slixmpp
from slixmpp.exceptions import IqError, IqTimeout

class Client(slixmpp.ClientXMPP):
    def __init__(self, jid, password, option=1, ):
        super().__init__(jid=jid, password=password)
        self.logged_user = jid
        self.process_action(option)

    def process_action(self, option):
        if (option == 1):
            self.add_event_handler("new_session", self.start)

    async def start(self):
        self.send_presence("chat", "Connected from Santiago's chat.")
        await self.get_roster()
