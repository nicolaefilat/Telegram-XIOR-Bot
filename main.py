import os
from threading import Thread
from time import sleep

from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.updater import Updater
from telegram.update import Update

from scraper import XiorScraper

PORT = int(os.environ.get('PORT', 8443))
telegram_token = os.environ.get("TG_TOKEN")


class TelegramHandler:

    def __init__(self):
        self.stop_thread = False
        self.running_thread = None
        self.scraper = XiorScraper()
        self.updater = Updater(telegram_token, use_context=True)

        dp = self.updater.dispatcher
        dp.add_handler(CommandHandler('start', self.start))
        dp.add_handler(CommandHandler('help', self.help))
        dp.add_handler(CommandHandler('run', self.run_delft))
        dp.add_handler(CommandHandler('check', self.run_normal_check))
        dp.add_handler(CommandHandler('stop', self.stop))

    def start_polling(self):
        self.updater.start_polling()

    def run_heroku(self):
        self.updater.start_webhook(listen="0.0.0.0",
                                   port=int(PORT),
                                   url_path=telegram_token,
                                   webhook_url='https://bot-delft-xior.herokuapp.com/' + telegram_token)

        self.updater.idle()

    def start(self, update: Update, context: CallbackContext):
        self.stop_thread = False
        update.message.reply_text(
            "Hello this is a xior bot that scrapes the https://www.xior-booking.com/# for Netherlands + Delft")
        running_thread = Thread(target=self.daemon_runner, args=(update, lambda: self.stop_thread))
        running_thread.start()

    def help(self, update: Update, context: CallbackContext):
        update.message.reply_text("""Available Commands 
• /start  - starts daemon
• /check - Checks on the main website if we can actually get something
• /help - Print this page
• /run - Checks offers for delft that do not require code
• /stop - Stops the bot""")

    def daemon_runner(self, update: Update, stop):
        time = 0
        while True:
            if self.stop_thread:
                break
            data = self.scraper.get_data_delft()
            if time > 30:
                update.message.reply_text(f"I have been trying for more than {time} seconds!")
                time = 0
            if len(data) > 0:
                update.message.reply_text(f"I got this data for *delft* \n *Check website!!* \n{data}",
                                          parse_mode='markdown')
            time += 30
            sleep(30)

    def run_delft(self, update: Update, context: CallbackContext):
        data = self.scraper.get_data_delft()
        if len(data) > 0:
            update.message.reply_text(f"I got this data for *delft* \n *Check website!!* \n{data}",
                                      parse_mode='markdown')
        else:
            update.message.reply_text("There is nothing for delft right now :(")

    def run_normal_check(self, update: Update, context: CallbackContext):
        data = self.scraper.get_working_data()
        if len(data) > 0:
            update.message.reply_text(f"I got this data for check data from Germany. \n{data}",
                                      parse_mode="markdown")
        else:
            update.message.reply_text("There is nothing for the whole website. Code might have crashed :(")

    def stop(self, update: Update, context: CallbackContext):
        self.stop_thread = True
        self.running_thread.join()
        update.message.reply_text("Stopped the daemon")


if __name__ == "__main__":
    # TelegramHandler().start_polling()
    TelegramHandler().run_heroku()
