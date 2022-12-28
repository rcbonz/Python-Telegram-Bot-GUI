#!/usr/bin/env python

from configparser import ConfigParser
from colorama import Back, Fore, Style
from datetime import datetime
import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    ContextTypes,
    MessageHandler,
    filters)
from telegram.constants import ParseMode, ChatAction

CONFIG_FILE = "settings/settings.ini"
config = ConfigParser()
config.read(CONFIG_FILE)
BOT_API_KEY = config["SETTINGS"]["BOT_API_KEY"]


def fr(msg):
	return Fore.RED + msg + Fore.RESET
def fg(msg):
	return Fore.GREEN + msg + Fore.RESET
def fy(msg):
	return Fore.YELLOW + msg + Fore.RESET
def fb(msg):
	return Fore.BLUE + msg + Fore.RESET
def fgb(msg):
	return Fore.GREEN + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL
def fyb(msg):
	return Fore.YELLOW + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL

def nowF(style="Time"):
    if style == "Time":
        return str(datetime.now().strftime("%H:%M:%S"))
    elif style == "Date":
        return str(datetime.now().strftime("%d/%m/%Y"))
    elif style == "DateTime":
        return str(datetime.now().strftime("%d/%m/%Y - %H:%M:%S"))
    elif style == "FolderName":
        return str(datetime.now().strftime("%Y.%m.%d-%H.%M"))

def out(msg, counter=" ", msg_type=0, end=False):
    if end == False:
        if msg_type == 1: # Positive message
            return print(f'\r[{counter}]' + fg("! ") + fy(str(nowF())) + (' - ') + str(msg))
        elif msg_type == 0: # Neutral message
            return print(f'\r[{counter}]  ' + fy(str(nowF())) + (' - ') + str(msg))
        elif msg_type == -1: # Negative message
            return print(f'\r[{counter}]' + fr("! ") + fy(str(nowF())) + (' - ') + str(msg))
        elif msg_type == 2: # Question message
            return print(f'\r[{counter}]' + fb("? ") + fy(str(nowF())) + (' - ') + str(msg))
    else:    
        if msg_type == 1: # Positive message
            return print(f'\r[{counter}]' + fg("! ") + fy(str(nowF())) + (' - ') + str(msg), end=end)
        elif msg_type == 0: # Neutral message
            return print(f'[{counter}]  ' + fy(str(nowF())) + (' - ') + str(msg), end=end)
        elif msg_type == -1: # Negative message
            return print(f'[{counter}]' + fr("! ") + fy(str(nowF())) + (' - ') + str(msg), end=end)
        elif msg_type == 2: # Question message
            return print(f'\r[{counter}]' + fb("? ") + fy(str(nowF())) + (' - ') + str(msg), end=end)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    person = update.message.from_user.first_name
    personId = update.message.from_user.id
    lng = update.message.from_user.language_code[:2]
    exists = False
    warned_list = open("postMaintWarn", "r").read().splitlines()
    for line in warned_list:
        if str(personId) == line.split(",")[0]:
            exists = True
            break
    out(f'Message received during maintenance from ' + fgb(str(person)) + " - " + fgb(str(personId)) + ': ' + fyb(str(update.message.text)) + " - have tried before: " + fgb(str(exists)) + ", lang: " + fgb(update.message.from_user.language_code))
    if exists == False:
        with open("postMaintWarn", "a+") as av:
            av.write(f"{personId},{lng}\n")
        message = "I'm still in maintenance.. I'll let you know when finished."
    else:
        message = "Hi, I'm under maintenance and will be back soon. I'll send you a message when I get back!"
    await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)

def main() -> None:
    out("Starting maintenance Bot...",msg_type=1)
    application = Application.builder().token(BOT_API_KEY).concurrent_updates(True).read_timeout(7).get_updates_read_timeout(42).build()
    out("Telegram Bot maintenance started.",msg_type=1)
    while not application.update_queue.empty():
        asyncio.create_task(application.process_update(Application.process_update()))
    application.add_handler(MessageHandler(filters.ALL, echo))
    application.run_polling(connect_timeout=20, pool_timeout=20, read_timeout=15, write_timeout=15)

if __name__ == '__main__':
    main()