"""
Universidad del Valle de Guatemala
(CC3067) Redes
Santiago Taracena Puga (20017)
Proyecto 1 - Protocolo XMPP
"""

from client import Client
from utils.register_new_user import register_new_user

if (__name__ == "__main__"):

    print("\n- * - XMPP Chat - * -\n")

    selected_option = str()

    while (selected_option != "3"):

        print("Main Options:\n\t1. Sign up to XMPP Chat.\n\t2. Sign in to XMPP Chat.\n\t3. Close XMPP Chat.\n\t4. Delete account on XMPP Chat.\n")
        selected_option = input("Please input the option you want to execute: ")

        if (selected_option == "1"):
            jid = input("\nInput your new JID please: ")
            password = input("Now please input your new password: ")
            status = register_new_user(jid, password)
            status_message = "\nYour sign up has been succesful!\n" if (status) else "\nYour sign up has thrown an error...\n"
            print(status_message)

        if (selected_option == "2"):
            jid = input("\nInput your JID please: ")
            password = input("Now please input your password: ")
            xmpp_client = Client(jid, password, option=1)
            xmpp_client.connect(disable_starttls=True, use_ssl=False)
            xmpp_client.process(forever=False)
