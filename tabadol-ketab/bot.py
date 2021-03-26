from telegram.ext import CommandHandler, Filters, MessageHandler, Updater, ConversationHandler
from validator_collection import is_not_empty

import setting
from models import TabadolKetab, Goodreads

GET_USERNAME_GOODREADS = 0
def search_a_book_by_only_name(update, context):
    update.message.reply_text(" بزار بگردم....")
    books = TabadolKetab().search_for_a_book(update.message.text)
    if not is_not_empty(books):
        update.message.reply_text("ای بابا. مثل اینکه این کتابو ندارن :(((((")
    for book in books:
        update.message.reply_text(book["book_details"])
    
def goodreads_books_in_tabadol_ketab_intro(update, context):    
    update.message.reply_text("""خب. حالا یوزرنیم Goodreadsیت رو بفرست.  \n\n\n مثلا: 129432286-revisto
    """)
    return GET_USERNAME_GOODREADS

def goodreads_books_in_tabadol_ketab_checker(update, context):
    books = TabadolKetab().search_for_books(Goodreads().get_want_to_read_books_names(update.message.text))
    if not is_not_empty(books):
        update.message.reply_text("ای بابا. مثل اینکه این کتابایی که تو Goodreadsیت هستنو ندارن :(((((")
    for book in books:
        update.message.reply_text(book)
    return ConversationHandler.END

def cancel(update, context):
    update.message.reply_text("حله")

    return ConversationHandler.END

def main():
    updater = Updater(setting.telegram_access_token, use_context=True)
    dp = updater.dispatcher

    #dp.add_handler(MessageHandler(Filters.text , search_a_book_by_only_name))
   
    goodreads_in_tabadolketab_converstation = ConversationHandler(
        entry_points=[CommandHandler('goodreadsbooksintabadol', goodreads_books_in_tabadol_ketab_intro)],
        states={
            GET_USERNAME_GOODREADS: [MessageHandler(Filters.text, goodreads_books_in_tabadol_ketab_checker)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(goodreads_in_tabadolketab_converstation)
    dp.add_handler(MessageHandler(Filters.text, search_a_book_by_only_name))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
