"""
Universidad del Valle de Guatemala
(CC3067) Redes
Santiago Taracena Puga (20017)
Proyecto 1 - Protocolo XMPP
"""

# Useful utilities for the chat file.
import asyncio
from utils.client import Client
from utils.delete import Delete
from utils.register_new_user import register_new_user

# If name equals main (good practice).
if (__name__ == "__main__"):

    # Allow async code to execute on Windows.
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Chat's title.
    print("\n- * - XMPP Chat - * -\n")

    # Instantiating a selected option.
    selected_option = str()

    # While loop to display the initial menu.
    while (selected_option != "3"):

        # Initial menu and selected option input.
        print("\nMain Options:\n\t1. Sign up to XMPP Chat.\n\t2. Sign in to XMPP Chat.\n\t3. Close XMPP Chat.\n\t4. Delete account on XMPP Chat.\n")
        selected_option = input("Please input the option you want to execute: ")

        # First case, to sign up into the class' server.
        if (selected_option == "1"):
            jid = input("\nInput your new JID please: ")
            password = input("Now please input your new password: ")
            status = register_new_user(jid, password)
            status_message = "\nYour sign up has been succesful!\n" if (status) else "\nYour sign up has thrown an error...\n"
            print(status_message)

        # Second case, to sign in into the class' server.
        elif (selected_option == "2"):
            jid = input("\nInput your JID please: ")
            password = input("Now please input your password: ")
            xmpp_client = Client(jid, password)
            xmpp_client.connect(disable_starttls=True, use_ssl=False)
            xmpp_client.process(forever=False)

        # Third case, to log out the class' server.
        elif (selected_option == "3"):
            print("\nSee you soon!\n")

        # Fourth case, to delete an account.
        elif (selected_option == "4"):
            jid = input("\nInput the JID to delete please: ")
            password = input("Now please input the password of that JID: ")
            xmpp_delete = Delete(jid, password)
            xmpp_delete.connect(disable_starttls=True, use_ssl=False)
            xmpp_delete.process(forever=False)

        # Base case, where the selected option is invalid.
        else:
            print("\nThe option you have selected is invalid.\n")
