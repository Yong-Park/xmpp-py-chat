"""
Universidad del Valle de Guatemala
(CC3067) Redes
Santiago Taracena Puga (20017)
Proyecto 1 - Protocolo XMPP
"""

# Important libraries to use.
import slixmpp
import asyncio
from aioconsole import ainput
from slixmpp.exceptions import IqError, IqTimeout

# Client class definition.
class Client(slixmpp.ClientXMPP):

    # Constructor method.
    def __init__(self, jid, password):
        super().__init__(jid=jid, password=password)
        self.logged_user = jid
        self.register_all_plugins()

    # Async function that starts the client.
    async def start(self):
        self.send_presence("chat", "Connected from Santiago's chat.")
        await self.get_roster()
        self.is_user_connected = True
        asyncio.create_task(self.process_action())

    # Async function to display the client"s menu and process actions.
    async def process_action(self):

        # While loop to display the menu while the user is connected.
        while (self.is_user_connected):

            # Client"s menu and option input.
            print("Chat Options:\n\t1. Show all my contacts.\n\t2. Show a contact info.\n\t3. Send contact request.\n\t4. Send a DM.\n\t9. Sign out.\n")
            selected_option = input("Please input the option you want to execute: ")

            # Option to show all contacts.
            if (selected_option == "1"):
                await self.show_all_contacts()

            # Option to show a specific contact.
            if (selected_option == "2"):
                await self.show_contact_info()

            # Option to send a contact request to a user.
            if (selected_option == "3"):
                await self.send_contact_request()

    # Async function to show all contacts.
    async def show_all_contacts(self):

        # Client roster containing the contacts.
        client_roster = self.client_roster

        # Returning nothing if no contacts found.
        if (not client_roster):
            print("No contacts found.")
            return

        # Iterating through the contacts.
        for contact in client_roster.keys():

            # If statement to continue if the contact finds itself.
            if (contact == self.boundjid.bare):
                continue

            # Show contact"s JID.
            print(f"\nContact JID: {contact}")

            # Iterating through the contact"s information.
            for _, presence in client_roster.presence(contact).items():

                # Show contact"s presence.
                presence_value = presence["show"] or "Connected from Santiago's chat!"
                print(f"Contact presence: {presence_value}")

                # Show contact"s status.
                status = presence["status"] or "None"
                print(f"Contact status: {status}")

    # Async function to show a contact by JID.
    async def show_contact_info(self):

        # Input to get the JID to request.
        contact_jid = input("Input the contact's JID please: ")

        # Client roster containing the contacts.
        client_roster = self.client_roster

        # Contact has not been found.
        found = False

        # Returning nothing if no contacts found.
        if (not client_roster):
            print("\nNo contacts found.")
            return

        # Iterating through the contacts.
        for contact in client_roster.keys():

            # If statement to continue if the contact finds itself.
            if (contact == contact_jid):

                # Contact has been found.
                found = True

                # Show contact"s JID.
                print(f"\nContact JID: {contact}")

                # Iterating through the contact"s information.
                for _, presence in client_roster.presence(contact).items():

                    # Show contact"s presence.
                    presence_value = presence["show"] or "Logged from Santiago's chat!"
                    print(f"Contact presence: {presence_value}")

                    # Show contact"s status.
                    status = presence["status"] or "None"
                    print(f"Contact status: {status}")

        # Text that shows if the contact was not found.
        if (not found):
            print("\nSeems like you haven't requested the user's contact...")

    # Async function that sends a contact request to someone.
    async def send_contact_request(self):

        # Input to get the new contact"s JID.
        contact_jid = input("Input your new contact's JID please: ")

        # Process to send a presence subscription.
        self.send_presence_subscription(contact_jid)
        print("Your request has been properly sent.")
        await self.get_roster()

    # Async function that sends a DM.
    async def send_dm(self):

        # Input for the JID to send a DM to.
        dm_to_jid = input("Please input the JID of the user you want to send a DM: ")
        self.current_chatting_jid = dm_to_jid

        # Show information about the chat.
        print(f"\nChatting with {dm_to_jid}.\nType \"exit\" to close the chat.\n")

        # While loop to keep chatting.
        while (True):

            # Async input to wait for the user"s message.
            message = await ainput("Type your message: ")

            # Message "exit" if user quits chatting.
            if (message == "exit"):
                self.current_chatting_jid = ""
                break

            # Send the message if it"s not the "exit" keyword.
            else:
                print(f"{self.user_jid.split('@')[0]}: {message}")
                self.send_message(mto=dm_to_jid, mbody=message, mtype="chat")

    # Function that registers all needed plugins.
    def register_all_plugins(self):

        # Plugin used to ping the server.
        self.register_plugin("xep_0199")

        # Plugin used to access service discovery.
        self.register_plugin("xep_0030")

        # Plugin used to submit data forms.
        self.register_plugin("xep_0004")

        # Plugin used to access MUC functionality.
        self.register_plugin("xep_0045")

        # Plugin used to access PubSub functionality.
        self.register_plugin("xep_0060")

        # Plugin used to get push notifications.
        self.register_plugin("xep_0085")

        # Plugin used to access out of band data.
        self.register_plugin("xep_0066")
        self.register_plugin("xep_0363")
