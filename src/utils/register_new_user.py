"""
Universidad del Valle de Guatemala
(CC3067) Redes
Santiago Taracena Puga (20017)
Proyecto 1 - Protocolo XMPP
"""

# Importing xmpp library.
import xmpp

# Function that registers a new user into the server.
def register_new_user(jid, password):

    # Connecting to the server.
    xmpp_jid = xmpp.JID(jid)
    xmpp_account = xmpp.Client(xmpp_jid.getDomain(), debug=[])
    xmpp_account.connect()

    # Status to create the account.
    xmpp_status = xmpp.features.register(
        xmpp_account,
        xmpp_jid.getDomain(),
        { "username": xmpp_jid.getNode(), "password": password }
    )

    # Return the account's creation casted to boolean.
    return bool(xmpp_status)
