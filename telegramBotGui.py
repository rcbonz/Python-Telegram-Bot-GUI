from tkinter import *
import threading
from datetime import datetime
import asyncio
from configparser import ConfigParser
import time
import telegram
from telegram.constants import ParseMode, ChatAction
import os
import functools
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from PIL import ImageTk,Image
from tkinter import font as tkFont

"GUI fonts"
class RichText(Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_font = tkFont.nametofont(self.cget("font"))
        default_font.config(family="Helvetica")
        reg_font = tkFont.Font(**default_font.configure())
        tini_font = tkFont.Font(**default_font.configure())
        italic_font = tkFont.Font(**default_font.configure())
        h1_font = tkFont.Font(**default_font.configure())
        reg_font.configure(family="Helvetica",size=12,weight="normal")
        tini_font.configure(family="Helvetica",size=8,weight="bold",slant="italic")
        italic_font.configure(family="Helvetica",size=12,weight="normal",slant="italic")
        h1_font.configure(family="Helvetica",size=17,weight="bold")
        self.tag_configure("center", font=reg_font,justify="center",background=dark4,spacing1=5,spacing2=5,spacing3=5)
        self.tag_configure("left", font=reg_font,background=dark4,spacing1=5,spacing2=5,spacing3=5)
        self.tag_configure("tinil", font=tini_font,background=dark4,spacing1=5,spacing2=5,spacing3=5)
        self.tag_configure("right", font=reg_font,justify="right",background=dark3,spacing1=5,spacing2=5,spacing3=5)
        self.tag_configure("tinir", font=tini_font,justify="right",background=dark3,spacing1=5,spacing2=5,spacing3=5)
        self.tag_configure("italic", font=italic_font,spacing1=5,spacing2=5,spacing3=5)
        self.tag_configure("h1", font=h1_font,spacing1=5,spacing2=5,spacing3=5)



CONFIG_FILE = "settings/settings.ini"
config = ConfigParser()
config.read(CONFIG_FILE)

BOT_API_KEY = config["SETTINGS"]["BOT_API_KEY"]
OWNER_TELE = config["SETTINGS"]["OWNER_TELE"]


dark5 = "#001019"
dark4 = "#002029"
dark3 = "#00303d"
dark2 = "#004052"
dark1 = "#005066"
clear1 = "#00607a"
yell1 = "#EAE8D7"


def nowF(style="DateTime"):
    if style == "Time":
        return str(datetime.now().strftime("%H:%M:%S"))
    elif style == "Date":
        return str(datetime.now().strftime("%d/%m/%Y"))
    elif style == "DateTime":
        return str(datetime.now().strftime("%d/%m/%Y - %H:%M:%S"))
    elif style == "FolderName":
        return str(datetime.now().strftime("%Y.%m.%d-%H.%M"))


def telegramMessage(message, photo=None, attat=None, err=False, chatId=OWNER_TELE):
    asyncio.run(telegramMessagesender(message, photo, attat, err, chatId))


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
            if "Timed out" in str(err):
                tmout_e_count += 1
                print(f"{err} count: {tmout_e_count}")
                if tmout_e_count > 3:
                    print(err)
                    return
                else:
                    continue
            else:
                print(err)
                return
        except KeyboardInterrupt:
            exit()


def create_conversations_frame_list(chatidd,perso):
    try:
        "Conversation History Frame"
        toexec = f"""
global conversation_frame_{chatidd}
conversation_frame_{chatidd} = Frame(conversations_frame, highlightthickness=0, borderwidth=0, relief='ridge', width=600, height=700, bg=dark2)
        """
        exec(toexec)
        toexec2 = f"""
global conversation_{chatidd}
conversation_{chatidd} = RichText(conversation_frame_{chatidd}, width=90, bg=dark4, fg=yell1)
"""
        exec(toexec2)
        exec(f"preimage{chatidd}=Image.open('userData/{chatidd}.gif').resize([35,35])")
        exec(f"image{chatidd}=ImageTk.PhotoImage(preimage{chatidd})")
        exec(f"title{chatidd} = Button(conversation_frame_{chatidd},image=image{chatidd},compound='left', highlightthickness=0, font='Helvetica 13 bold', text=f'  |  {perso}', bg=dark5, fg=yell1,command=functools.partial(toggle_entry,chatidd,perso))")
        exec(f"title{chatidd}.photo = image{chatidd}")

        exec(f"title{chatidd}.place(x=2, width=570, relheight=0.05)")
        exec(f"file_button{chatidd} = Button(conversation_frame_{chatidd}, text='↥', font='Helvetica 14 bold',highlightthickness=0, bg=dark4, fg=yell1, command=functools.partial(send_file))")
        exec(f"file_button{chatidd}.place(x=570,y=0,width=30, relheight=0.05)")
        exec(f"conversation_{chatidd}.place(relwidth=0.98, relheight=0.95,rely=0.05)")
        exec(f"scrollbar_{chatidd} = Scrollbar(conversation_frame_{chatidd}, bg=dark4, troughcolor=dark2)")
        exec(f"scrollbar_{chatidd}.place(relheight=0.95, relx=0.98,rely=0.05)")
        exec(f"scrollbar_{chatidd}.config(command=conversation_{chatidd}.yview)")
        exec(f"conversation_frame_{chatidd}.place(relwidth=1,relheight=1)")
        exec(f"conversation_{chatidd}.insert(END, '[{nowF()}] {perso}: Conversation started'+ '\\n','center')")
        chathist = open(f"chats/{chatidd}_{perso}_chat_pers").read().splitlines()
        for line in chathist[-25:]:
            msg_time = line.split("]")[0][1:]
            msgm = line.split("]")[1].split(":")[1][1:]
            global last_talk
            if "GUIBot:" in line:
                if last_talk == "guibot":
                    exec(f"conversation_{chatidd}.insert(END, f'{msgm}     \\n','right')")
                else:
                    exec(f"conversation_{chatidd}.insert(END, f'{msg_time}    \\n','tinir')")
                    exec(f"conversation_{chatidd}.insert(END, f'{msgm}     \\n','right')")
                    last_talk = "guibot"
            else:
                if last_talk == "notguibot":
                    exec(f"conversation_{chatidd}.insert(END, f'   {msgm} \\n','left')")
                else:
                    exec(f"conversation_{chatidd}.insert(END, f'  {msg_time}\\n','tinil')")
                    exec(f"conversation_{chatidd}.insert(END, f'   {msgm}\\n','left')")
                    last_talk = "notguibot"
        exec(f"conversation_{chatidd}.see(END)")
        print(f"[ ] Created chat {chatidd}")
    except Exception as err:
        print("create_frame_list: " + str(err))
        time.sleep(1)


def window():
    root.deiconify()
    root.title("Telegram Bot Chat")
    root.resizable(width=False, height=False)
    global sv
    sv = StringVar()
    global conversations_frame
    conversations_frame = Frame(content, highlightthickness=0, borderwidth=0, relief='ridge', width=600, height=700, bg=dark2)
    conversations_frame.grid(column=1, row=1, columnspan=2)
    "Title Frame"
    title_frame = Frame(content, borderwidth=0, relief="ridge", width=800, height=50, bg=dark4)
    title = Label(title_frame, highlightthickness=0, font="Helvetica 18 bold", text="GUIBot Talk",width=2, height=3, bg=dark4, fg=yell1)
    title.place(relwidth=1, relheight=1)
    "Contacts Frame"
    contact_list_frame = Frame(content, borderwidth=0, relief="ridge", width=200, height=750, bg=dark5)
    global contact_list_content_frame
    contact_list_content_frame = Frame(contact_list_frame, bg=dark5)
    contact_list_content_frame.place(relwidth=1, relheight=1)
    "Message to Send Frame"
    messa_frame = Frame(content, borderwidth=0, relief="ridge", width=500, height=50, bg=dark3)
    global messa
    messa = Entry(messa_frame, width=50, bg=dark3, fg=yell1, border=0,font="Helvetica 13",textvariable=sv)
    messa.place(relwidth=1, relheight=1)
    messa.bind('<Return>',lambda e: sendButton(messa.get(),chatid))
    "Send Button Frame"
    send_frame = Frame(content, borderwidth=0, relief="ridge", width=100, height=50)
    send_bt = Button(send_frame, text="Send", font="Helvetica 10 bold", bg=dark4, fg=yell1, width=100, height=50, border=0, command=lambda: sendButton(messa.get(),chatid))
    send_bt.place(relwidth=1, relheight=1)
    "Grid Formation"
    content.grid(column=0, row=0)
    contact_list_frame.grid(column=0, row=1, columnspan=1, rowspan=2)
    title_frame.grid(column=0, row=0, columnspan=3)
    messa_frame.grid(column=1, row=2)
    send_frame.grid(column=2, row=2)
    messa.focus()
    "Start getting chats"
    global rcc
    rcc = threading.Thread(target=get_chats)
    rcc.start()
    time.sleep(1)
    "Start receiving messages"
    global rcv
    rcv = threading.Thread(target=get_messages)
    rcv.start()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


"Function to start a thread for sending messages"
def sendButton(msg, chatidd):
    msg = msg
    messa.delete(0, END)
    mesg = f"[{nowF()}] GUIBot: {msg}"
    global last_talk
    if last_talk == "guibot":
        exec(f"conversation_{chatidd}.insert(END, f'{msg}     \\n','right')")
    else:
        exec(f"conversation_{chatidd}.insert(END, f'{nowF()}    \\n','tinir')")
        exec(f"conversation_{chatidd}.insert(END, f'{msg}     \\n','right')")
        last_talk = "guibot"
    exec(f"conversation_{chatid}.see(END)")
    with open(f"chats/{chatid}_{person}_chat_pers", "a+") as ch:
        ch.write(mesg+"\n")
    print(f"Message: {msg}")
    telegramMessage(msg,chatId=chatidd)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        print("[ ] Closing window..")
        root.destroy()
        thr_event.set()


def send_file():
    filename = askopenfilename()
    if len(filename) > 2:
        with open(filename, 'rb') as f:
            if filename.split(".")[-1] in ["png","jpg","jpeg","gif"]:
                telegramMessage(message=filename.split("/")[-1], chatId=chatid, photo=f)
            else:
                telegramMessage(message=filename.split("/")[-1],chatId=chatid, photo='doc', attat=f)
        mesg = f"[{nowF()}] GUIBot: {filename.split('/')[-1]} enviado."
        exec(f"conversation_{chatid}.insert(END, mesg + '\\n')")
        exec(f"conversation_{chatid}.see(END)")
        with open(f"chats/{chatid}_{person}_chat_pers", "a+") as ch:
            ch.write(mesg+"\n")


def toggle_newmessage(chat,sta):
    exec(f"global newmessages_{chat}")
    if sta == "read":
        exec(f"newmessages_{chat}.place_forget()")
    elif chat != chatid:
        exec(f"newmessages_{chat}.place(x=180,y=27)")


"Function to get messages"
def get_messages():
    sv1 = ""
    while True:
        try:
            if sv1 != sv.get() and sv.get() != "":
                telegramMessage(message=False,chatId=chatid)
                sv1 = sv.get()
            for filename in os.listdir("chats/"):
                if len(os.path.splitext(filename)[0].split("_")) == 3:
                    mesgs = open(f"chats/{filename}").read().splitlines()
                    for i, mesg in enumerate(mesgs):
                        if mesg.split("|||")[1] == "ur":
                            messag = mesg.split("|||")[0]
                            if "Arquivo recebido:" in messag:
                                print("arquivo recebido")
                            preimage=Image.open("src/new_message.gif")
                            image=ImageTk.PhotoImage(preimage)
                            toggle_newmessage(filename.split('_')[0],"new")
                            print(f"New message: {filename.split('_')[0]} - {messag}")
                            global last_talk
                            msg_time = messag.split("]")[0][1:]
                            msgm = messag.split("]")[1].split(":")[1][1:]
                            if last_talk == "notguibot":
                                exec(f"conversation_{filename.split('_')[0]}.insert(END, f'   {msgm} \\n','left')")
                            else:
                                exec(f"conversation_{filename.split('_')[0]}.insert(END, f'  {msg_time}\\n','tinil')")
                                exec(f"conversation_{filename.split('_')[0]}.insert(END, f'   {msgm}\\n','left')")
                                last_talk = "notguibot"
                            mesgs.pop(i)
                            with open(f'chats/{filename}', 'w') as f:
                                for line in mesgs:
                                    f.write(line + '\n')
                if thr_event.is_set():
                    print("[ ] get_messages killed...")
                    exit()
                time.sleep(0.2)
        except Exception as err:
            print("Getmessages: " + str(err))
            time.sleep(1)


def toggle_entry(chat,perso):
    toggle_newmessage(chat,"read")
    global person
    person = perso
    global chatid
    chatid = chat
    for cha in chat_lil:
        if cha != f"conversation_frame_{chat}":
            exec(f"{cha}.place_forget()")
        else:
            exec(f"conversation_frame_{chat}.place(relwidth=1,relheight=1)")


def get_chats():
    chats = {}
    a = 0
    while True:
        try:
            for filename in os.listdir("chats/"):
                if len(os.path.splitext(filename)[0].split("_")) == 3:
                    chats[(os.path.splitext(filename)[0].split("_")[0])] = (os.path.splitext(filename)[0].split("_")[1])
            for chat, perso in chats.items():
                if not f"conversation_frame_{chat}" in chat_lil:
                    create_button(perso,chat,a)
                    create_conversations_frame_list(chat,perso)
                    chat_lil.append(f"conversation_frame_{chat}")
                    a += 62
            time.sleep(1)
            if thr_event.is_set():
                print("[ ] get_chats killed...")
                break
        except Exception as err:
            print("get_chats: " + str(err))
            time.sleep(1)


eval_link = lambda chat, perso: (lambda p: toggle_entry(chat,perso))


def create_button(perso,chat,a):
        texta = f"\n   {perso}\n          {chat}\n"
        exec(f"global button_frame{chat}")
        exec(f'button_frame{chat} = Frame(contact_list_content_frame, borderwidth=0, relief="ridge", width=200, height=62)')
        exec(f'button{chat} = Button(button_frame{chat}, cursor="hand2", compound="left", font="Helvetica 10 bold",bg=dark4,fg=yell1,text=texta, width=200, height=3,command=functools.partial(toggle_entry,chat,perso))')
        exec(f'preimage{chat}=Image.open("userData/{chat}.gif")')
        exec(f'image{chat}=ImageTk.PhotoImage(preimage{chat})')
        exec(f'avat{chat} = Label(button_frame{chat}, cursor="hand2",image=image{chat},bd=0)')
        exec(f"avat{chat}.photo = image{chat}")
        exec(f'avat{chat}.bind("<Button-1>", eval_link(chat,perso))')
        exec(f"prenewmessageimage=Image.open('src/new_message.gif')")
        exec(f"newmessageimage=ImageTk.PhotoImage(prenewmessageimage)")
        exec(f"""
global newmessages_{chat}
newmessages_{chat} = Label(button_frame{chat},image=newmessageimage,bd=0)""")
        exec(f"newmessages_{chat}.photo = newmessageimage")
        exec(f"newmessages_{chat}.bind('<Button-1>', eval_link(chat,perso))")
        exec(f"newmessages_{chat}.place(x=180,y=27)")
        exec(f"newmessages_{chat}.place_forget()")
        exec(f'button_frame{chat}.place(relwidth=1,y=a)')
        exec(f'button{chat}.place(relwidth=1,relheight=1)')
        exec(f'avat{chat}.place(x=1,y=1)')
        global chatid
        chatid = chat
        global person
        person = perso
        return


while True:
    open_janela = input("Enter to start and open the window:")
    if open_janela == "":
        root = Tk()
        "MAIN Frame"
        last_talk = ""
        content = Frame(root)
        thr_event = threading.Event()
        chatid = ""
        chat_lil = []
        window()
    else:
        print("[ ] Exiting...")
        exit()



