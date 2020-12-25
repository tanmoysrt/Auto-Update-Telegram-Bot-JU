import argparse
import time
from telegram import *
import db_commands


parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-name_id", "--NameId", help = "name_id of notice db")
parser.add_argument("-t", "--Type", help= "Type Of User -- private/group")
parser.add_argument("-token", "--Token", help="Token For Bot")

# Read arguments from command line
args = parser.parse_args()


MAX_MESSAGE_LENGTH = 4090

# Templates
title_bar  = '''<b>🔔🔔 JU {} Update 🔔🔔</b>\n<a>------------------------------</a>\n<b>Top 5 Notices | For More : <a href="http://www.jaduniv.edu.in/">Click Here</a></b>\n<a>------------------------------</a>\n'''
notice_title = '''<b><i>🟢<a href="{}">{}</a></i></b>\n\n'''
divider = '''<a>------------------------------</a>\n'''
sublink = '''<a href="{}"> ➡️<i> {}</i></a>\n'''
ju = '''<b>🔔🔔 JU Homepage Update 🔔🔔</b>\n <a>------------------------------</a>\n<a href="http://www.jaduniv.edu.in/">➡️<i>    Click Here To Visit    </i>⬅️</a>\n <a>------------------------------</a>'''

def buildMessage(name_id,end):
    if name_id == "ju":
        return ju
    ending = 0
    message = ""
    data = db_commands.getJuNoticeSectionsSelectedData(name_id)
    if len(data)> end:
        ending = end
    else : ending = len(data)
    message+=title_bar.format(str(name_id).title())
    for i in range(ending):
        title = data[i]['title']
        link = data[i]['link']
        sublinks = data[i]['sublinks']
        message+=notice_title.format(link,title)
        for j in sublinks.items():
            message+=sublink.format(j[1],j[0])
        message+=divider
    return message

def send_message(bot, chat_id, text: str):
    if len(text) <= MAX_MESSAGE_LENGTH:
        bot.send_message(chat_id, text,parse_mode=ParseMode.HTML)
        print(f"Sent to {str(chat_id)}")
        return

    parts = []
    while len(text) > 0:
        if len(text) > MAX_MESSAGE_LENGTH:
            part = text[:MAX_MESSAGE_LENGTH]
            first_lnbr = part.rfind('\n')
            if first_lnbr != -1:
                parts.append(part[:first_lnbr])
                text = text[first_lnbr:]
            else:
                parts.append(part)
                text = text[MAX_MESSAGE_LENGTH:]
        else:
            parts.append(text)
            break

    for part in parts:
        bot.send_message(chat_id, part,parse_mode=ParseMode.HTML)
        time.sleep(1)

    print(f"Sent to {str(chat_id)}")
    return


def sendMessageInBulk(token,type,text):
    bot = Bot(token)

    if type == "private":
        users = db_commands.getTelegramUsers()
        for i in users:
            try:
                send_message(bot,int(i[2]),text)
            except Exception as e:
                print(text)
                print(f'Fail To Send {e}')
            time.sleep(0.5)

    elif type == "group" :
        groups = db_commands.getTelegramGroups()
        for i in groups:
            try:
                send_message(bot,int(i[2]),text)
            except Exception as e:
                print(f'Fail To Send {e}')
    else:
        print("Fail To Send")

if args.Type and args.NameId and args.Token:
    text = buildMessage(args.NameId,5)
    sendMessageInBulk(args.Token,args.Type,text)
