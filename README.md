# Python-Telegram-Bot GUI

### Using
```
git clone https://github.com/rcbonz/Python-Telegram-Bot-GUI.git
```
```
cd Python-Telegram-Bot-GUI
```

```
pip install -r requirements.txt
```
Fill the /settings/settings.ini with your information (how to get those info? see [bellow](https://github.com/rcbonz/Python-Telegram-Bot-GUI/edit/main/README.md#how-to-create-a-telegram-bot))
```
BOT_API_KEY = <Your bot API Key>
OWNER_TELE = <Bot's owner Telegram ID>
```

In two separate terminals run:

1. The bot:
```
python3 guiBot.py
```

2.  The GUI:
```
python3 telegramBotGui.py
```

#### How to create a Telegram Bot
-   Start a conversation with [BotFather](https://t.me/BotFather);
-   Send it to the BotFather: /newbot
-   Choose a name for your bot;
-   Choose a username for your bot;
-   Done! You'll get a token to access the HTTP API.

#### How to get channel or chat (contact) ID from Telegram
-   Start a conversation with [JsonDumpBot](https://t.me/JsonDumpBot);
-   It will reply with a json with information from the message;
-   Go to the channel or chat you want the id and forward a message from there to JsonDumpBot;
-   Find the id in the reply. It'll look something like this:
```html
   {...
    "forward_from_chat": {
          "id": xxxxxxxxx,
   ...}
```


### What is it?
This project aims to provide a base with wich you can have a *G*raphical *U*ser *I*nterface conversation with the bot users. You shoud be able to build your bot over this base. It was writen based on [PTB](https://github.com/python-telegram-bot/python-telegram-bot) library.

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
