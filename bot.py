from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, CallbackQueryHandler, Filters

from dictionary import Dictionary

import re


class Bot:
    def __init__(self):
        self.d = Dictionary()
        self.main()

    @staticmethod
    def is_eng(word) -> bool:
        return re.match(r'^[a-zA-Z]+\Z', word) is not None

    @staticmethod
    def start_command(update: Update, context: CallbackContext) -> None:
        update.message.reply_text('Hello')

    @staticmethod
    def help_command(update: Update, context: CallbackContext) -> None:
        update.message.reply_text('Help')

    def dictionary(self, update: Update, context: CallbackContext) -> None:
        word = update.message.text.lower()

        if self.is_eng(word):
            typ, result, uk, us = self.d.search(word)
            if typ == 'word':
                text = f"<b>{word}</b>\n\n"
                keyboard = [
                    [InlineKeyboardButton('🇬🇧', url=uk), InlineKeyboardButton('🇺🇸', url=us)]
                ]

                for x in result:
                    text = text + x + '\n'

                update.message.reply_text(text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))
            else:
                text = "Choose: "
                keyboard = []
                i = 0
                for key, value in result.items():
                    if int(i % 2) == 0:
                        keyboard.append([InlineKeyboardButton(key, callback_data=key)])
                    if int(i % 2) == 1:
                        keyboard[int(i / 2)].append(InlineKeyboardButton(key, callback_data=key))
                    i += 1

                if len(keyboard) > 0:
                    update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard, resize_keyboard=True))
                else:
                    update.message.reply_text('No Result')

        else:
            update.message.reply_text('Invalid Input\n\n'
                                      '<i>(Persian Translation Is Not Supported Yet)</i>', parse_mode='HTML')

    def callback_handler(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()

        typ, result, uk, us = self.d.search(query.data, is_word_search=True)

        text = f"<b>{query.data}</b>\n\n"
        keyboard = [
            [InlineKeyboardButton('🇬🇧', url=uk), InlineKeyboardButton('🇺🇸', url=us)]
        ]

        for x in result:
            text = text + x + '\n'

        if text:
            query.edit_message_text(text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            query.edit_message_text("IDK Why, But Bad Request\n\n"
                                    "I Will Fix This Later")

    def main(self):
        updater = Updater('TOKEN', use_context=True)
        dpa = updater.dispatcher.add_handler

        dpa(CommandHandler('start', self.start_command))
        dpa(CommandHandler('start', self.help_command))
        dpa(MessageHandler(Filters.text & ~Filters.command, self.dictionary))
        dpa(CallbackQueryHandler(self.callback_handler))

        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    Bot()
