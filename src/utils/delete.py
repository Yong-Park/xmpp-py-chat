"""
Universidad del Valle de Guatemala
(CC3067) Redes
Santiago Taracena Puga (20017)
Proyecto 1 - Protocolo XMPP
"""

# Important libraries to use.
import slixmpp
from slixmpp.xmlstream.stanzabase import ET

# Delete class definition (with slixmpp.ClientXMPP).
class Delete(slixmpp.ClientXMPP):

    # Constructor method.
    def __init__(self, jid, password):
        super().__init__(jid=jid, password=password)
        self.user_to_delete = jid
        self.add_event_handler("session_start", self.start)

    # Async function that starts the client.
    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        await self.delete_account()
        self.disconnect()

    # Funcion para desregistrar cuenta ====================================================================================================================================
    async def delete_account(self):

        # Response from the server.
        response = self.Iq()
        response["from"] = self.boundjid.user
        response["type"] = "set"

        # Stanza to delete the account.
        fragment = ET.fromstring(
            "<query xmlns='jabber:iq:register'><remove/></query>"
        )

        # Appending the stanza to delete the account.
        response.append(fragment)

        # Account has been deleted succesfully.
        await response.send()
        deleted_user = self.boundjid.jid.split("/")[0]
        print(f"\nThe account {deleted_user} has been deleted succesfully.\n")
