# Python-Telegram-Bot GUI

### Using
Soon requirements.txt will be available.

### What is it?
This project aims to provide a base with wich you can have a *G*raphical *U*ser *I*nterface conversation with the bot users. You shoud be able to build your bot over this base.

![Art](https://github.com/rcbonz/Python-Telegram-Bot-GUI/blob/main/gui.png)

### Functionalities
* GUI for chatting with bot users;
* Send document or photos through GUI;
* Indication of new messages in chats;
* A maintenance script that warns users about it;
* After a maintenance, it'll automatically warn who tried to talk to it that it's back;
* A simple start menu with one option: send message to the bot owner.

### How it works
Tkinter provides a very flexible library to build GUI on python. Unfortunately I'm not a programmer and when I started trying to make it work, I knew nothing about Tkinter. Not much changed, yet something that actually seems to work could be built.

It consists in two separated scripts, one that runs the bot (if you already have one, you can change few lines of code and use the GUI script) and the other that actually brings the GUI to life.

Since I'm only a noob and my knoledge is limited to what I've had time to learn, there are many subjects that could have a better approach. For instance, instead of running an actual database, it relies on text files that feed the GUI and keep the conversations history.

### To do
If you have ideas on how to improve this code, please feel free to submit a pull request.
* Clean and improve Tkinter code;
* Add more chat functionalities;
* Add admin functionalities (i.e. ban/unban an user from a drop down menu)

### Licence
GPL-3.0
