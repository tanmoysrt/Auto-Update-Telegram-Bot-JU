from telegram import *
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
import db_commands
from dotenv import load_dotenv
import os
import  send_messages_telegram


load_dotenv()
telegram_token = os.getenv("BOT_TOKEN")
bot = Bot(telegram_token)
updater = Updater(telegram_token, use_context=True)

def getHelpLines():
    helplines='''<b><u>Welcome You</u></b>\n<b><i>These Commands are available</i></b>\n<a>---------------------</a>\n'''
    helplines+= "<a>/register - To Register Yourself/Group To All Updates</a>\n"
    helplines+= "<a>/registerme - To Register Yourself To All Updates</a>\n"
    helplines+= "<a>---------------------</a>\n"
    helplines+= "<a>/menu - To Get List Of Options</a>\n"
    helplines+= "<a>/juupdate - To Get The List Of Update's Topic</a>\n"
    helplines+= "<a>/help - To Get List Of Commands</a>\n"
    helplines+= "<a>---------------------</a>\n"
    return helplines

def sendTelegramMessage(chat_id, text):
    try:
        bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=ParseMode.HTML
        )
        return True
    except:
        return False

def start(update: Update, context: CallbackContext):
    if update.message.chat.type == "private":
        name = str(update.message.chat.first_name)+" "+str(update.message.chat.last_name)
        if db_commands.insertRecordTelegramUser(update.message.chat.id,name):
            bot.send_message(
                chat_id=update.message.chat_id,
                text=f'Hi 😎 {name}. You have successfully registered 🎉🎉'
            )
            bot.send_message(
                chat_id=update.message.chat_id,
                text='Wish You 🎅🍰 Merry Christmas Day 🍰🎅'
            )
            bot.send_message(
                chat_id=update.message.chat_id,
                text=getHelpLines(),
                parse_mode=ParseMode.HTML
            )
            keyboard = [[
                InlineKeyboardButton("Check JU Updates", callback_data='check_updates_ju_options'),
            ]]

            # creating a reply markup of inline keyboard options
            reply_markup = InlineKeyboardMarkup(keyboard)

            # sending the message to the current chat id
            update.message.reply_text('Choose a option to continue :', reply_markup=reply_markup)
        else:
            bot.send_message(
                chat_id=update.message.chat_id,
                text=f'Failed! Please Retry'
            )
    elif update.message.chat.type == "group" :
        if db_commands.insertRecordTelegramGroup(update.message.chat.id,update.message.chat.title):
            bot.send_message(
                chat_id=update.message.chat_id,
                text=f'🎉🎉 {update.message.chat.title} group has successfully registered ! 🎉🎉'
            )
            bot.send_message(
                chat_id=update.message.chat_id,
                text='Wish You All 🎅🍰 Merry Christmas Day 🍰🎅'
            )
            bot.send_message(
                chat_id=update.message.chat_id,
                text=getHelpLines(),
                parse_mode=ParseMode.HTML
            )
            keyboard = [[
                InlineKeyboardButton("Check JU Updates", callback_data='check_updates_ju_options'),
            ]]

            # creating a reply markup of inline keyboard options
            reply_markup = InlineKeyboardMarkup(keyboard)

            # sending the message to the current chat id
            update.message.reply_text('Choose a option to continue :', reply_markup=reply_markup)
        else:
            bot.send_message(
                chat_id=update.message.chat_id,
                text=f'Failed! Please Retry'
            )
    else:
        pass

def registerme(update: Update, context: CallbackContext):
    if update.message.chat.type == "private":
        name = str(update.message.chat.first_name)+" "+str(update.message.chat.last_name)
        if db_commands.insertRecordTelegramUser(update.message.chat.id,name):
            bot.send_message(
                chat_id=update.message.chat_id,
                text=f'Hi 😎 {name}. You have successfully registered 🎉🎉'
            )
            bot.send_message(
                chat_id=update.message.chat_id,
                text='Wish You 🎅🍰 Merry Christmas Day 🍰🎅'
            )
        else:
            bot.send_message(
                chat_id=update.message.chat_id,
                text=f'Failed! Please Retry'
            )
    elif update.message.chat.type == "group" :
        if db_commands.insertRecordTelegramGroup(update.message.chat.id,update.message.chat.title):
            bot.send_message(
                chat_id=update.message.chat_id,
                text=f'🎉🎉 {update.message.chat.title} group has successfully registered ! 🎉🎉'
            )
            bot.send_message(
                chat_id=update.message.chat_id,
                text='Wish You All 🎅🍰 Merry Christmas Day 🍰🎅'
            )
        else:
            bot.send_message(
                chat_id=update.message.chat_id,
                text=f'Failed! Please Retry'
            )
        if db_commands.insertRecordTelegramUser(update.message.from_user.id,str(update.message.chat.first_name)+" "+str(update.message.chat.last_name)):
            bot.send_message(
                chat_id=update.message.chat_id,
                text=f'Hi 😎 {str(update.message.chat.first_name)+" "+str(update.message.chat.last_name)}. You have successfully registered 🎉🎉'
            )
            bot.send_message(
                chat_id=update.message.chat_id,
                text='Wish You 🎅🍰 Merry Christmas Day 🍰🎅'
            )
        else:
            bot.send_message(
                chat_id=update.message.chat_id,
                text=f'Failed! Please Retry'
            )
    else:
        pass

def showOptions(update: Update, context: CallbackContext):
    keyboard = [[
        InlineKeyboardButton("Check JU Updates", callback_data='check_updates_ju_options'),
    ]]

    # creating a reply markup of inline keyboard options
    reply_markup = InlineKeyboardMarkup(keyboard)

    # sending the message to the current chat id
    update.message.reply_text('Choose a option to continue :', reply_markup=reply_markup)
    pass

def showJUUpdatesSection(query=None,update=None):
    keyboard = [[
        InlineKeyboardButton("Admission", callback_data="admission_update"),
        InlineKeyboardButton("Fellowship",callback_data="fellowship_update")
    ],
    [
        InlineKeyboardButton("Events",callback_data="events_update"),
        InlineKeyboardButton("Recruitment",callback_data="recruitment_update")
    ],
    [
        InlineKeyboardButton("Circular",callback_data="circular_update"),
        InlineKeyboardButton("Reports",callback_data="reports_update")
    ],
    [
        InlineKeyboardButton("<< Back To Options",callback_data="back_to_options")
    ]
    ]

    # creating a reply markup of inline keyboard options
    reply_markup = InlineKeyboardMarkup(keyboard)

    if query != None:
        query.edit_message_text("Select Topic To Get The Recent Update : ")
        query.edit_message_reply_markup(reply_markup=reply_markup)
    elif update !=None:
        update.message.reply_text("Select Topic To Get The Recent Update : ",reply_markup=reply_markup)

def pass_request_to_showJUUpdatesSection(update: Update, context: CallbackContext):
    showJUUpdatesSection(update=update)

def showOptionsAgain(query):
    keyboard = [[
        InlineKeyboardButton("Check JU Updates", callback_data='check_updates_ju_options'),
    ]]

    # creating a reply markup of inline keyboard options
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("Choose a option to continue : ")
    query.edit_message_reply_markup(reply_markup=reply_markup)

def buttonClick(update: Update, context: CallbackContext):
    query: CallbackQuery = update.callback_query
    query.answer()
    context.bot.send_chat_action(chat_id=query.message.chat_id, action=ChatAction.TYPING)
    if query.data == "check_updates_ju_options":
        showJUUpdatesSection(query=query)
    elif query.data == "back_to_options":
        showOptionsAgain(query=query)
    elif query.data == "admission_update":
        msg = send_messages_telegram.buildMessage("admission",5)
        send_messages_telegram.send_message(bot,query.message.chat_id,msg)
    elif query.data == "fellowship_update":
        msg = send_messages_telegram.buildMessage("fellowship", 5)
        send_messages_telegram.send_message(bot, query.message.chat_id, msg)
    elif query.data == "events_update":
        msg = send_messages_telegram.buildMessage("events", 5)
        send_messages_telegram.send_message(bot, query.message.chat_id, msg)
    elif query.data == "recruitment_update":
        msg = send_messages_telegram.buildMessage("recruitment", 5)
        send_messages_telegram.send_message(bot, query.message.chat_id, msg)
    elif query.data == "circular_update":
        msg = send_messages_telegram.buildMessage("circular", 5)
        send_messages_telegram.send_message(bot, query.message.chat_id, msg)
    elif query.data == "reports_update":
        msg = send_messages_telegram.buildMessage("report", 5)
        send_messages_telegram.send_message(bot, query.message.chat_id, msg)

def help(update: Update, context: CallbackContext):

    bot.send_message(
        chat_id=update.message.chat_id,
        text=getHelpLines(),
        parse_mode=ParseMode.HTML
    )

def main():
    print("Starting Telegram Bot.....")
    dp = updater.dispatcher

    # COMMANDS HANDLER
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('register',start))
    dp.add_handler(CommandHandler('registerme',registerme))
    dp.add_handler(CommandHandler('menu',showOptions))
    dp.add_handler(CommandHandler('juupdate',pass_request_to_showJUUpdatesSection))
    dp.add_handler(CommandHandler('help',help))
    dp.add_handler(CallbackQueryHandler(buttonClick))


    updater.start_polling()
    print("Bot is waiting for user input")
    updater.idle()
    print("Bot is exiting.")

if __name__ == '__main__':
    main()
