# xmpp-py-chat

### Description.

Welcome to `xmpp-py-chat`. The Asynchronous XMPP Client project aims to create a robust and feature-rich XMPP (Extensible Messaging and Presence Protocol) client using the Python programming language. The client will leverage the capabilities of two prominent XMPP libraries, xmpppy and slixmpp, along with the asyncio framework to achieve high-performance, non-blocking communication.

### Features.

This project consisted on developing a lot of cool and useful features that any chat that implements the XMPP protocol. They will be mentioned on the following list.

Account administration:
- [x] Sign up
- [x] Sign in
- [x] Logout
- [x] Account deletion

Communication:
- [x] Show all contacts
- [x] Show contact info
- [x] Add new contacts
- [x] Direct communication
- [x] Group communication
- [x] Presence update
- [x] Notifications
- [x] File messages

### Instalation.

The most important thing to notice is that this project has been developed on Python 3.11.4. The first thing you have to check is if you have Python 3.11.* installed on your computer. You can check it executing the command `python --version` on any terminal.

Next, you have to make sure to install every needed library that's been used on the project. First you have to clone this repository and then access the "xmpp-py-chat" folder that contains all the source code and miscellaneous files. Inside that folder, you have to execute the following commands.

```sh
pip install xmpppy
pip install --upgrade xmpppy
pip install slixmpp
pip install --upgrade slixmpp
pip install asyncio
pip install --upgrade asyncio
pip install aiohttp
pip install --upgrade aiohttp
pip install aioconsole
pip install --upgrade aioconsole
```

To ensure you have installed every single needed library.

Finally, you just have to execute the command `python chat.py` inside the "src" folder to execute the project.

### Development difficulties.

The most challenging aspect of developing this project was undoubtedly navigating the intricate landscape of asynchronous programming. Dealing with multiple concurrent tasks, from real-time message delivery to presence updates and file sharing, demanded a deep understanding of the intricacies of asynchronous design. Coordinating and synchronizing these tasks using the asyncio framework, while ensuring non-blocking execution and maintaining data integrity, proved to be a significant hurdle. Nevertheless, overcoming these complexities allowed the project to achieve its goal of creating a robust and responsive XMPP client that capitalizes on the power of asynchronous communication, offering users a seamless and efficient messaging experience.

### Learned lessons.

Overall, this project provided a comprehensive education in asynchronous programming techniques, protocol integration, and user-centered design, leaving me better equipped to tackle complex, real-time applications in the future. I really learned a lot about asynchronous programming and libraries like asyncio, and even it was the toughest part to implement I think I really learned a lot about it and that's really valuable to me.


### How to run the flooding code in this one

Once you loggin, you the option 8 will be displayed called, "Send messeage to another node (user)". In which after pressing 8 and enter. It will ask you to write the jid user to send it to. In which later it wil ask the message that you want to send it. After that just press Enter, and you will be able to see for the user jid the poped message. For this case its necesary that all the user jids in this case lets represent them as nodes, to be connected, else for the logig that flooding contains it will not be able to send the data to the other nodes, since one of them that its a road to get to the node destination is not online, the message it will never arrive, until that node gets online. 