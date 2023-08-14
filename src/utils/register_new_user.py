"""
Universidad del Valle de Guatemala
(CC3067) Redes
Santiago Taracena Puga (20017)
Proyecto 1 - Protocolo XMPP
"""

import xmpp

def register_new_user(jid, password):

    xmpp_jid = xmpp.JID(jid)
    xmpp_account = xmpp.Client(xmpp_jid.getDomain(), debug=[])
    xmpp_account.connect()

    xmpp_status = xmpp.features.register(
        xmpp_account,
        xmpp_jid.getDomain(),
        { "username": xmpp_jid.getNode(), "password": password }
    )

    return bool(xmpp_status)
