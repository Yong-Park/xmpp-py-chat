"""
Universidad del Valle de Guatemala
(CC3067) Redes
Santiago Taracena Puga (20017)
Proyecto 1 - Protocolo XMPP
"""

# Important libraries to use.
import slixmpp
import asyncio
import base64
from aioconsole import ainput

# Client class definition (with slixmpp.ClientXMPP).
class Client(slixmpp.ClientXMPP):

    # Constructor method.
    def __init__(self, jid, password):
        super().__init__(jid=jid, password=password)
        self.logged_user = jid
        self.current_chatting_jid = ""
        self.is_user_connected = False
        self.group = ""
        self.register_all_plugins()
        self.register_all_handlers()

    # Async function that starts the client.
    async def start(self, event):
        self.send_presence("chat", "Connected from Santiago's chat.")
        await self.get_roster()
        self.is_user_connected = True
        asyncio.create_task(self.process_action())

    # Async function to display the client's menu and process actions.
    async def process_action(self):

        # While loop to display the menu while the user is connected.
        while (self.is_user_connected):

            # Client"s menu and option input.
            print("\nChat Options:\n\t1. Show all my contacts.\n\t2. Show a contact info.\n\t3. Send contact request.\n\t4. Send a DM.\n\t5. Send a group message.\n\t6. Update your presence.\n\t8. Sign out.\n")
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

                elif (group_option == "2"):
                    group_to_join = input("Please input the group's name: ")
                    await self.join_group(group_to_join)

                elif (group_option == "3"):
                    continue

            # Option to change presence status and message.
            elif (selected_option == "6"):
                await self.update_presence()

            # Option to send a file to a contact.
            elif (selected_option == "7"):
                await self.send_file()

            # Option to disconnect from the session.
            elif (selected_option == "8"):
                self.disconnect()
                self.is_user_connected = False

            # If no correct option was picked, it shows.
            else:
                print("\nYou have not picked a correct option.\n")

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
            presence_value = "Offline"
            status = "None"

            # Iterating through the contact's information.
            for _, presence in client_roster.presence(contact).items():

                # Show contact's presence.
                presence_value = presence["show"] or "Offline"

                # Show contact's status.
                status = presence["status"] or "None"

            # Show contact's results.
            print(f"Contact presence: {presence_value}")
            print(f"Contact status: {status}\n")

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
                presence_value = "Offline"
                status = "None"

                # Iterating through the contact's information.
                for _, presence in client_roster.presence(contact).items():

                    # Show contact's presence.
                    presence_value = presence["show"] or "Offline"

                    # Show contact's status.
                    status = presence["status"] or "None"

                # Show contact's results.
                print(f"Contact presence: {presence_value}")
                print(f"Contact status: {status}\n")

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

            # Async input to wait for the user's message.
            message = await ainput("Type your message: ")

            # Message "exit" if user quits chatting.
            if (message == "exit"):
                self.current_chatting_jid = ""
                break

            # Send the message if it's not the "exit" keyword.
            else:
                print(f"{self.logged_user.split('@')[0]}: {message}")
                self.send_message(mto=dm_to_jid, mbody=message, mtype="chat")

    # Async function that handles message reception.
    async def receive_message(self, message):

        # Check it the message is actually a chat message.
        if (message["type"] == "chat"):

            emitter = str(message["from"])
            actual_emitter = emitter.split("/")[0]

            if (actual_emitter == self.current_chatting_jid):
                print(f"\n{actual_emitter}: {message['body']}")
            else:
                print(f"\n<!> New message from {actual_emitter}.\n")

    # Async function to handle user's presence.
    async def handle_presence(self, presence):

        # Process to handle the accepted request.
        if (presence["type"] == "subscribe"):
            self.send_presence_subscription(pto=presence["from"], ptype="subscribed")
            await self.get_roster()
            print(f"\n<!> {presence['from']} has accepted your request.\n")

        # If there's not a presence requrest.
        else:
            if (self.is_user_connected):
                if (presence["type"] == "available"):
                    self.display_presence_message(presence, True)
                elif (presence["type"] == "unavailable"):
                    self.display_presence_message(presence, False)
                else:
                    self.display_presence_message(presence)

    # Function to process the display presence message.
    def display_presence_message(self, presence, available=None):
        actual_boundjid = str(presence["from"]).split("/")[0]
        if (self.boundjid.bare != actual_boundjid):
            state = "available" if (available) else presence["show"] if (available is None) else "offline"
            if (presence["status"] != ""):
                print(f"\n<!> {actual_boundjid} is {state} with status {presence['status']}.\n")
            else:
                print(f"\n<!> {actual_boundjid} is {state}.\n")

    # Function to send a custom failed auth message.
    def failed_auth(self, event):
        self.disconnect()
        print("\nThe account you tried to sign in doesn't exist.\n")

    # Async function to notify a group's message.
    async def message_received(self, message):

        # Message emitter.
        emitter = message["mucnick"]

        # Notification process.
        if (emitter != self.boundjid.user):
            print(f"\n<!> {emitter} in {message['from']}: {message['body']}\n")

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

    # Async function to update your presence in the chat.
    async def update_presence(self):

        # Status state to show its respective color.
        status = input("\nPresence options:\n\t1. Available\n\t2. Idle\n\t3. Busy\n\t4. Do Not Disturb\n\nChoose your option: ")

        # Conditions to change the status color.
        if (status == "1"):
            presence = "chat"
        elif (status == "2"):
            presence = "away"
        elif (status == "3"):
            presence = "xa"
        elif (status == "4"):
            presence = "dnd"
        else:
            presence = "chat"

        # Input to enter your description message.
        description = input("Now please input your description message: ")

        # Updating the user's presence.
        self.send_presence(pshow=presence, pstatus=description) 
        await self.get_roster() 

    # Async function to send a file.
    async def send_file(self):

        # Inputs to get the info about the file that's about to be sent.
        receptor = input("Please input the JID of the user you wanna send the file to: ")
        file_path = input("Now please input the path of the file you wanna send: ")

        # Splitting the file path to get the extension.
        file_extension = file_path.split(".")[-1]

        # Opening and reading the file.
        file = open(file_path, "rb")
        file_data = file.read()

        # Sending the encoded file.
        file_encoded_data = base64.b64encode(file_data).decode()
        print("file_encoded_data", file_encoded_data)
        self.send_message(mto=receptor, mbody=f"file://{file_extension}://{file_encoded_data}", mtype="chat")

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

        # Failed auth event handler.
        self.add_event_handler("failed_auth", self.failed_auth)

        # Message event handler.
        self.add_event_handler("message", self.receive_message)

        # Presence request handler.
        self.add_event_handler("presence", self.handle_presence)

        # Group chat message handler.
        self.add_event_handler("groupchat_message", self.message_received)
