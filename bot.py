from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler
from dictionary import Dictionary


class Bot:
    def __init__(self):
        self.d = Dictionary()
        self.main()

    @staticmethod
    def start_command(update: Update, context: CallbackContext) -> None:
        update.message.reply_text('Hemlo')

    @staticmethod
    def help_command(update: Update, context: CallbackContext) -> None:
        update.message.reply_text('Help')

    def dictionary(self, update: Update, context: CallbackContext) -> None:
        word = update.message.text.lower().strip()

    def main(self):
        updater = Updater('TOKEN')
        dpa = updater.dispatcher.add_handler



