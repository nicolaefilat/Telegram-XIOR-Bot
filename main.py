from threading import Thread
from time import sleep

from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.updater import Updater
from telegram.update import Update

import scraper

updater = Updater("5389706742:AAHyWq3hmLXTFShnt33ZdLGBzArRQ4ZmreU", use_context=True)
stop_thread = False
running_thread = None


def start(update: Update, context: CallbackContext):
    global stop_thread
    global running_thread
    stop_thread = False
    update.message.reply_text(
        "Hello this is a xior bot that scrapes the https://www.xior-booking.com/# for Netherlands + Delft")
    running_thread = Thread(target=daemon_runner, args=(update, lambda: stop_thread))
    running_thread.start()


def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :-
    /check - Checks on the main website if we can actually get something
    /help - Print this page
    /runDelft - Runs check on delft
    /stop - Stops the bot""")


def daemon_runner(update: Update, stop):
    time = 0
    while True:
        if stop():
            break
        data = scraper.get_delft()
        if time > 3600 * 2:
            update.message.reply_text(f"I have been trying for more than 2 hours and still nothing")
            time = 0
        if len(data) > 0:
            update.message.reply_text(f"I got this data for *delft* \n *Check website!!* \n{data}",
                                      parse_mode='markdown')
        time += 20
        sleep(20)


def run_delft(update: Update, context: CallbackContext):
    data = scraper.get_delft()
    if len(data) > 0:
        update.message.reply_text(f"I got this data for *delft* \n *Check website!!* \n{data}", parse_mode='markdown')
    else:
        update.message.reply_text("There is nothing for delft right now :(")


def run_normal_check(update: Update, context: CallbackContext):
    data = scraper.get_working_data()
    if len(data) > 0:
        update.message.reply_text(f"I got this data for normal website\n *Check website!!* \n{data}",
                                  parse_mode="markdown")
    else:
        update.message.reply_text("There is nothing for the whole website. Code might have crashed :(")


def stop(update: Update, context: CallbackContext):
    global stop_thread
    stop_thread = True

    running_thread.join()
    update.message.reply_text(
        "Stopped the daemon")


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('runDelft', run_delft))
updater.dispatcher.add_handler(CommandHandler('check', run_normal_check))
updater.dispatcher.add_handler(CommandHandler('stop', stop))

updater.start_polling()
