from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from validator_collection import is_not_empty

import setting
from models import TabadolKetab

def search_a_book_by_only_name(update, context):
    update.message.reply_text(" بزار بگردم....")
    books = TabadolKetab().search_for_a_book(update.message.text)
    if not is_not_empty(books):
        update.message.reply_text("ای بابا. مثل اینکه این کتابو ندارن :(((((")
    for book in books:
        update.message.reply_text(book["book_details"])

def main():
    updater = Updater(setting.telegram_access_token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text , search_a_book_by_only_name))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
