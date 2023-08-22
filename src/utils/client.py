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

# Client class definition (with slixmpp.ClientXMPP).
class Client(slixmpp.ClientXMPP):

    # Constructor method.
    def __init__(self, jid, password):
        super().__init__(jid=jid, password=password)
        self.logged_user = jid
        self.current_chatting_jid = ""
        self.group = ""
        self.register_all_plugins()
        self.register_all_handlers()

    # Async function that starts the client.
    async def start(self):
        self.send_presence("chat", "Connected from Santiago's chat.")
        await self.get_roster()
        self.is_user_connected = True
        asyncio.create_task(self.process_action())

    # Async function to display the client's menu and process actions.
    async def process_action(self):

        # While loop to display the menu while the user is connected.
        while (self.is_user_connected):

            # Client"s menu and option input.
            print("Chat Options:\n\t1. Show all my contacts.\n\t2. Show a contact info.\n\t3. Send contact request.\n\t4. Send a DM.\n\t5. Send a group message.\n\t8. Sign out.\n")
            selected_option = input("Please input the option you want to execute: ")

            # Option to show all contacts.
            if (selected_option == "1"):
                await self.show_all_contacts()

            # Option to show a specific contact.
            elif (selected_option == "2"):
                await self.show_contact_info()

            # Option to send a contact request to a user.
            elif (selected_option == "3"):
                await self.send_contact_request()

            # Option to send a DM to a user.
            elif (selected_option == "4"):
                await self.send_dm()

            # Option to send a message on a groupal chat.
            elif (selected_option == "5"):

                print("\nGroup Chat Options:\n\t1. Create group.\n\t2. Join group.\n\t3. Exit.\n")
                group_option = input("Please input the option you want to execute: ")

                if (group_option == "1"):
                    group_to_create = input("Please input the group's name: ")
                    await self.create_group(group_to_create)

                elif (group_option == "3"):
                    continue

            # Option to change presence status and message.
            elif (selected_option == "6"):
                raise NotImplementedError()

            # Option to send a file to a contact.
            elif (selected_option == "7"):
                raise NotImplementedError()

            # Option to disconnect from the session.
            elif (selected_option == "8"):
                self.disconnect()
                self.is_user_connected = False

            # If no correct option was picked, it shows.
            else:
                print("\nYou have not picked a correct option.\n")

    # Async function that handles message reception.
    async def receive_message(self, message):

        # Check it the message is actually a chat message.
        if (message["type"] == "chat"):

            emitter = message["from"]

            if (emitter == self.current_chatting_jid):
                print(f"{emitter}: {message['body']}")
            else:
                print(f"New message from {emitter}.")

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

            # Show contact's JID.
            print(f"\nContact JID: {contact}")

            # Predetermined values.
            presence_value = "Available"
            status = "None"

            # Iterating through the contact's information.
            for _, presence in client_roster.presence(contact).items():

                # Show contact's presence.
                presence_value = presence["show"] or "Available"

                # Show contact's status.
                status = presence["status"] or "None"

            # Show contact's results.
            print(f"Contact presence: {presence_value}")
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

                # Show contact's JID.
                print(f"\nContact JID: {contact}")

                # Predetermined values.
                presence_value = "Available"
                status = "None"

                # Iterating through the contact's information.
                for _, presence in client_roster.presence(contact).items():

                    # Show contact's presence.
                    presence_value = presence["show"] or "Available"

                    # Show contact's status.
                    status = presence["status"] or "None"

                # Show contact's results.
                print(f"Contact presence: {presence_value}")
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

    # Async function to create a group chat.
    async def create_group(self, group_name):
        try:
            self.plugin["xep_0045"].join_muc(group_name, self.boundjid.user)
            form = self.plugin["xep_0004"].make_form(ftype="submit", title="Group chat configuration")
            form["muc#roomconfig_roomname"] = group_name
            form["muc#roomconfig_persistentroom"] = "1"
            form["muc#roomconfig_publicroom"] = "1"
            form["muc#roomconfig_membersonly"] = "0"
            form["muc#roomconfig_allowinvites"] = "0"
            form["muc#roomconfig_enablelogging"] = "1"
            form["muc#roomconfig_changesubject"] = "1"
            form["muc#roomconfig_maxusers"] = "64"
            form["muc#roomconfig_whois"] = "anyone"
            form["muc#roomconfig_roomdesc"] = "Group created from Santiago's chat."
            form["muc#roomconfig_roomowners"] = [self.boundjid.user]
            await self.plugin["xep_0045"].set_room_config(group_name, config=form)
            print(f"Group {group_name} has been created.")
        except:
            print("\nHa ocurrido un error creando la sala.\n")

    # Async function to join a group chat.
    async def join_group(self, group_name):

        # Group name to send the message.
        self.group = group_name
        
        # Method to join the group.
        await self.plugin["xep_0045"].join_muc(room=group_name, nick=self.boundjid.user)

        # Show information about the group.
        print(f"\nChatting in {group_name}.\nType \"exit\" to close the chat.\n")

        # While loop to keep chatting.
        while (True):

            # Async input to wait for the user's message.
            message = await ainput("Type your message: ")

            # Messsage "exit" if user quits chatting.
            if (message == "exit"):
                self.current_chatting_jid = ""
                self.plugin["xep_0045"].leave_muc(room=group_name, nick=self.boundjid.user)
                self.group = ""
                break

            # Send the message if it's not the "exit" keyword.
            else:
                print(f"{self.logged_user.split('@')[0]}: {message}")
                self.send_message(mto=group_name, mbody=message, mtype="groupchat")

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

    # Function that registers all needed handlers.
    def register_all_handlers(self):

        # Session start event handler.
        self.add_event_handler("session_start", self.start)

        # Message event handler.
        self.add_event_handler("message", self.receive_message)

        self.add_event_handler('disco_items', self.print_rooms)
        self.add_event_handler('groupchat_message', self.chatroom_message)
        self.add_event_handler('presence', self.presence_handler)

