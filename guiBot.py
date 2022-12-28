#!/usr/bin/env python

from configparser import ConfigParser
import asyncio
from colorama import Back, Fore, Style
from datetime import datetime
import logging
from pathlib import Path
from pathlib import Path
from PIL import Image
import telegram
from telegram import Update
from telegram.ext import (
    Application,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters)
from telegram.constants import ParseMode, ChatAction


def setup_logger(loggerName, logFile, level=logging.INFO):
    l = logging.getLogger(loggerName)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fileHandler = logging.FileHandler(logFile)#, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)  


setup_logger('messages', 'log/messages.log')
messages = logging.getLogger('messages')

setup_logger('errors', 'log/errors.log')
errors = logging.getLogger('errors')


CONFIG_FILE = "settings/settings.ini"
config = ConfigParser()
config.read(CONFIG_FILE)

BOT_API_KEY = config["SETTINGS"]["BOT_API_KEY"] # The bot API KEY
OWNER_TELE = config["SETTINGS"]["OWNER_TELE"] # User ID of bot's owner


MESSAGE = range(1)


"Enable logging"
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.ERROR, filename="log/bot.log")
logger = logging.getLogger(__name__)


"https://manytools.org/hacker-tools/ascii-banner/"
LOGO = """
                  d8b 888888b.            888    
                  Y8P 888  "88b           888    
                      888  .88P           888    
 .d88b.  888  888 888 8888888K.   .d88b.  888888 
d88P"88b 888  888 888 888  "Y88b d88""88b 888    
888  888 888  888 888 888    888 888  888 888    
Y88b 888 Y88b 888 888 888   d88P Y88..88P Y88b.  
 "Y88888  "Y88888 888 8888888P"   "Y88P"   "Y888 
     888                                         
Y8b d88P                                         
 "Y88P"                                                                                                
"""


"Terminal out color funcs"
def fr(msg):
	return Fore.RED + msg + Fore.RESET
def fg(msg):
	return Fore.GREEN + msg + Fore.RESET
def fy(msg):
	return Fore.YELLOW + msg + Fore.RESET
def fb(msg):
	return Fore.BLUE + msg + Fore.RESET
def fc(msg):
	return Fore.CYAN + msg + Fore.RESET
def fm(msg):
	return Fore.MAGENTA + msg + Fore.RESET
def frb(msg):
	return Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL
def fgb(msg):
	return Fore.GREEN + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL
def fyb(msg):
	return Fore.YELLOW + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL
def fbb(msg):
	return Fore.BLUE + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL
def fcb(msg):
	return Fore.CYAN + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL
def fmb(msg):
	return Fore.MAGENTA + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL
def br(msg):
	return Back.RED + msg + Back.RESET
def bg(msg):
	return Back.GREEN + msg + Back.RESET
def by(msg):
	return Back.YELLOW + msg + Back.RESET
def bb(msg):
	return Back.CYAN + msg + Back.RESET


"Different time/date stamps function"
def nowF(style="Time"):
    if style == "Time":
        return str(datetime.now().strftime("%H:%M:%S"))
    elif style == "Date":
        return str(datetime.now().strftime("%d/%m/%Y"))
    elif style == "DateTime":
        return str(datetime.now().strftime("%d/%m/%Y - %H:%M:%S"))
    elif style == "FolderName":
        return str(datetime.now().strftime("%Y.%m.%d-%H.%M"))


"Printing nicely instead of just print()"
def out(msg, counter=" ", msg_type=0, end=False):
    if end == False:
        if msg_type == 1: # Positive message
            return print(f'\r[{counter}]' + fg("! ") + fy(str(nowF())) + (' - ') + str(msg))
        elif msg_type == 0: # Neutral message
            return print(f'\r[{counter}]  ' + fy(str(nowF())) + (' - ') + str(msg))
        elif msg_type == -1: # Negative message
            return print(f'\r[{counter}]' + fm("! ") + fy(str(nowF())) + (' - ') + str(msg))
        elif msg_type == 2: # Question message
            return print(f'\r[{counter}]' + fb("? ") + fy(str(nowF())) + (' - ') + str(msg))
    else:    
        if msg_type == 1: # Positive message
            return print(f'\r[{counter}]' + fg("! ") + fy(str(nowF())) + (' - ') + str(msg), end=end)
        elif msg_type == 0: # Neutral message
            return print(f'[{counter}]  ' + fy(str(nowF())) + (' - ') + str(msg), end=end)
        elif msg_type == -1: # Negative message
            return print(f'[{counter}]' + fm("! ") + fy(str(nowF())) + (' - ') + str(msg), end=end)
        elif msg_type == 2: # Question message
            return print(f'\r[{counter}]' + fb("? ") + fy(str(nowF())) + (' - ') + str(msg), end=end)


"A workaround to avoid using async on all functions. ;-P"
def telegramMessage(message, photo=None, attat=None, err=False, chatId=OWNER_TELE):
    asyncio.run(telegramMessagesender(message, photo, attat, err, chatId))


"Function to send messages, documents, photos and actions independently of an update on PTB"
async def telegramMessagesender(message, photo=None, attat=None, err=False, chatId=OWNER_TELE):
    tmout_e_count = 0
    while True:
        try:
            bot = telegram.Bot(token=BOT_API_KEY)
            async with bot:
                if message == False:
                    await bot.sendChatAction(chat_id=chatId, action=ChatAction.TYPING)
                elif photo == None and attat == None:
                    await bot.send_message(chatId, text=message, parse_mode=ParseMode.MARKDOWN,read_timeout=7,connect_timeout=7)
                elif photo == "doc":
                    await bot.sendChatAction(chat_id=chatId, action=ChatAction.UPLOAD_DOCUMENT)
                    await bot.send_document(chatId,document=attat, caption=message)
                elif photo != None:
                    await bot.sendChatAction(chat_id=chatId, action=ChatAction.UPLOAD_PHOTO)
                    await bot.send_photo(chat_id=chatId, photo=photo, caption=message)
                else:
                    await bot.send_message(chatId, text=message, parse_mode=ParseMode.MARKDOWN)
                return
        except Exception as err:
            "Try 3 times if timeout error"
            if "Timed out" in str(err):
                tmout_e_count += 1
                print(f"{err} count: {tmout_e_count}")
                if tmout_e_count > 3:
                    print(err)
                    return
                else:
                    continue
            else:
                return
        except KeyboardInterrupt:
            exit()

"/start menu"
async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_chat_action(action=ChatAction.TYPING)
        person = update.message.from_user.first_name
        personId = update.message.from_user.id # This is the ID used to identify people
        lastnam = update.message.from_user.last_name
        username = update.message.from_user.username
        user_photo = Path(f"userData/{personId}_{person}_{lastnam}_{username}.jpg")
        if not user_photo.is_file():
            result = await update.message.from_user.get_profile_photos(limit=1)
            photos = result['photos']
            if photos:
                photo = await application.bot.get_file(photos[0][-1]['file_id'])
                await photo.download(f"userData/{personId}_{person}_{lastnam}_{username}.jpg")
                origi = Image.open(f"userData/{personId}_{person}_{lastnam}_{username}.jpg").resize([60,60])
                origi.save(f"userData/{personId}.gif")
                out(fgb("Profile picture") + " from " + fyb(str(personId)) + " - " + fyb(str(person)) + " downloaded.")
            else:
                "If user doesn't have an image, use a generic one."
                origi = Image.open(f"userData/noimage.gif")
                origi.save(f"userData/{personId}.gif")
        out(fgb(person) + " - " + fgb(str(personId)) + " sent " + fyb(update.message.text))
        await update.message.reply_text("Start menu\n\n/message", parse_mode=ParseMode.MARKDOWN)
        return ConversationHandler.END
    except Exception as err:
        print(err)
        await update.message.reply_text('Error.', parse_mode=ParseMode.MARKDOWN)
        errors.error(err)
    except KeyboardInterrupt:
        out("Exiting..")
        exit()



"Messaged displayed after user send /message asking what the message is"
async def mensagem_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    person = update.message.from_user.first_name
    personId = update.message.from_user.id
    out(fgb(person) + " - " + fgb(str(personId)) + " sent " + fyb(update.message.text))
    await update.message.reply_text("What is the message you want to send to developers?\n\n/cancel", parse_mode=ParseMode.MARKDOWN)
    return MESSAGE


"Function that handles the message sent by user on previous func"
async def msgm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_chat_action(action=ChatAction.TYPING)
        person = update.message.from_user.first_name
        personId = update.message.from_user.id
        out(fgb(person) + " - " + fgb(str(personId)) + " sent " + fyb(update.message.text))
        if update.message.text in ["/cancelar","cancel"]:
            await update.message.reply_text("No problems!\n\n/start", parse_mode=ParseMode.MARKDOWN)
            return ConversationHandler.END
        message = f"{person} [{personId}] - '{update.message.text}'"
        await telegramMessagesender(message, photo=None, err=False, chatId=OWNER_TELE)
        msg = "Your message was successfully sent!\n\n/start"
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
        return ConversationHandler.END
    except Exception as err:
        print(err)
        errors.error(err)
        await update.message.reply_text('Error.', parse_mode=ParseMode.MARKDOWN)
        return ConversationHandler.END


"The echo function, but instead of echoing, it saves the message to be displayed on GUI."
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    person = update.message.from_user.first_name
    personId = update.message.from_user.id
    out(f'Message received from ' + fgb(str(person)) + " - " + fgb(str(personId)) + ': ' + fyb(str(update.message.text)))
    resposta = update.message.text
    with open(f"chats/{personId}_{person}_chat", "a+") as ch:
        ch.write(f"[{nowF(style='DateTime')}] {person}: {resposta}|||ur\n")
    with open(f"chats/{personId}_{person}_chat_pers", "a+") as ps:
        ps.write(f"[{nowF(style='DateTime')}] {person}: {resposta}\n")
    if resposta.lower() in command_list:
        message = "Did you mean:" + "\n\n/" + resposta.lower()
    await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)


"Handle attacthments"
async def echoattachment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    "Stores the attachment."
    out("Attachment received")
    try:
        person = update.message.from_user.first_name
        something = update.message.from_user._get_attrs(include_private=True,recursive=True)
        personId = update.message.from_user.id
        file_attrs = update.message.effective_attachment._get_attrs(include_private=True,recursive=True)
        att_file = await update.message.effective_attachment.get_file()
        await att_file.download(f"{personId}_{file_attrs['file_name']}")
        with open(f"chats/{personId}_{person}_chat", "a+") as ch:
            ch.write(f"[{nowF(style='DateTime')}] {person}:  Sent a file: {personId}_{file_attrs['file_name']}, {file_attrs['mime_type']} |||ur\n")
        with open(f"chats/{personId}_{person}_chat_pers", "a+") as ps:
            ps.write(f"[{nowF(style='DateTime')}] {person}: Sent a file: {personId}_{file_attrs['file_name']}, {file_attrs['mime_type']}\n")
    except Exception as err:
        print(err)

"Handle photos sent to bot"
async def echophoto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the photo."""
    out("Photo received")
    try:
        person = update.message.from_user.first_name
        personId = update.message.from_user.id
        file_attrs = update.message.photo[-1]._get_attrs(include_private=True,recursive=True)
        photo_file = await update.message.photo[-1].get_file()
        await photo_file.download(f"{personId}_{file_attrs['file_unique_id'][:7]}.jpg")
        with open(f"chats/{personId}_{person}_chat", "a+") as ch:
            ch.write(f"[{nowF(style='DateTime')}] {person}: Sent a photo: {personId}_{file_attrs['file_unique_id'][:7]}.jpg |||ur\n")
        with open(f"chats/{personId}_{person}_chat_pers", "a+") as ps:
            ps.write(f"[{nowF(style='DateTime')}] {person}:  Sent a photo: {file_attrs['file_unique_id'][:7]}.jpg\n")
    except Exception as err:
        print(err)



command_list = ["start","Start","cancel","cancelar"]


def main() -> None:
    "Create the Application and pass it your bot's token."
    out("Starting HeleaTelegram Bot...",msg_type=1)
    global application
    application = Application.builder().token(BOT_API_KEY).concurrent_updates(True).connect_timeout(10).read_timeout(17).pool_timeout(10).get_updates_read_timeout(42).build()
    out("Telegram Bot started.",msg_type=1)

    while not application.update_queue.empty():
        print("startigjob")
        asyncio.create_task(application.process_update(Application.process_update()))

    "Commands"
    application.add_handler(CommandHandler(["start","Start"], start_callback))
    application.add_handler(MessageHandler(filters.PHOTO, echophoto))
    application.add_handler(MessageHandler(filters.ATTACHMENT, echoattachment))

    "Handler for MESSAGE sending"
    conv_handler = ConversationHandler(entry_points=[CommandHandler(["mensagem","message"], mensagem_callback)],
        states={MESSAGE: [MessageHandler(filters.TEXT, msgm)],},
        fallbacks=[CommandHandler(["inicio","start","cancelar","cancel"], start_callback)],)
    application.add_handler(conv_handler)

    application.add_handler(MessageHandler(filters.ALL, echo))

    application.run_polling(connect_timeout=20, pool_timeout=20, read_timeout=15, write_timeout=15)




if __name__ == '__main__':
    print(fc(LOGO))
    out("Initializing system...",msg_type=1)
    "Firstly, let all people that tryed to talk to bot while in maintenance that it's back"
    warn_list = open("postMaintWarn", "r").read().splitlines()
    for line in warn_list:
        telegramMessage("I'm back!\n\n/start", photo=None, err=False, chatId=line.split(",")[0])
    with open("postMaintWarn","w") as au:
        au.write("")
    main()
