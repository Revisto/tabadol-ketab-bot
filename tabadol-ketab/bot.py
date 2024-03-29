from telegram.ext import CommandHandler, Filters, MessageHandler, Updater, ConversationHandler
from validator_collection import is_not_empty

import setting
from models import TabadolKetab, Goodreads

GET_USERNAME_GOODREADS = 0
GET_BOOKS_NAMES = 0
def search_a_book_by_only_name(update, context):
    update.message.reply_text(" بزار بگردم....")
    books = TabadolKetab().search_for_a_book(update.message.text, update)
    if not is_not_empty(books):
        update.message.reply_text("ای بابا. مثل اینکه این کتابو ندارن :(((((")
    
def goodreads_search_multiple_books_intro(update, context):
    if context.user_data.get("goodreads_id") is not None:
        update.message.reply_text(f"""خب. حالا یوزرنیم Goodreadsیت رو بفرست یا.  \n\n\n اگر میخوای با این یوزرنیم {context.user_data.get("goodreads_id")} پیش بری 1 رو بفرست.
        """)
    else:
        update.message.reply_text("""خب. حالا یوزرنیم Goodreadsیت رو بفرست.  \n\n\n مثلا: 129432286-revisto
        """)
    return GET_USERNAME_GOODREADS

def search_books_in_tabadol_ketab_intro(update, context):    
    update.message.reply_text("""خب حالا اسم کتابایی که میخوای سرچ کنم رو برام بفرست و بین هر اسم یه اینتر بزن :)  \n\n\n مثلا:\n\nهر روز\nناطوردشت\nشازده کوچولو\nسیزده دلیل برای این که
    """)
    return GET_BOOKS_NAMES

def search_multiple_books(update, context):
    update.message.reply_text(" بزار بگردم....")
    books = update.message.text
    multiple_books_list = books.split("\n")
    TabadolKetab().search_for_books_and_send_book_names_immediately(multiple_books_list, update)
    return ConversationHandler.END

def goodreads_books_in_tabadol_ketab_checker(update, context):
    update.message.reply_text("بزن بریم تو کارش. شاید یکمی طول بکشه...")
    goodreads_username = update.message.text
    if goodreads_username == "1" or goodreads_username == "۱":
        goodreads_username = context.user_data.get("goodreads_id")
    else:
        context.user_data["goodreads_id"] = goodreads_username
    goodreads_books = Goodreads().get_want_to_read_books_names(update.message.text)
    if not is_not_empty(goodreads_books):
        update.message.reply_text("یا یوزرنیمتو اشتباه وارد کردی, یا هیچ کتابی تو دسته want to readیت نداری :((((")
        return ConversationHandler.END
    update.message.reply_text("این کتابایی هستن که شما میخواین بخونین. تا دقایقی دیگه نتیجه رو بهتون میگم:")
    goodreads_books_message = ""
    for goodreads_book in goodreads_books:
        if len(goodreads_books_message) + len(goodreads_book) > 3800:
            update.message.reply_text(goodreads_books_message)
            goodreads_books_message = ""
        goodreads_books_message += f"{goodreads_book}\n"
    books = TabadolKetab().search_for_books_and_send_book_names_immediately(goodreads_books, update)
    if not is_not_empty(books):
        update.message.reply_text("ای بابا. مثل اینکه این کتابایی که تو Goodreadsیت هستنو ندارن :(")
    return ConversationHandler.END

def start(update, context):
    update.message.reply_text("خب. سلااااام.\n\nبا این بات چیکارا میتونی بکنی؟ \nمیتونی اسم کتابو بفرستو و من بهت بگم که آیا توی تبادل موجود هست یا نه.\n\nمیتونی این کامند رو بزنی و بعد یوزرنیم گودریدزتو بدی بهم تا همه کتابای want to read گودریدزتو چک کنم و بهت بگم کدوما توی تبادل موجوده. /goodreadsbooksintabadol")

def cancel(update, context):
    update.message.reply_text("حله")
    return ConversationHandler.END


def main():
    updater = Updater(setting.telegram_access_token, use_context=True)
    dp = updater.dispatcher
   
    goodreads_in_tabadolketab_converstation = ConversationHandler(
        entry_points=[CommandHandler('goodreadsbooksintabadol', goodreads_search_multiple_books_intro)],
        states={
            GET_USERNAME_GOODREADS: [MessageHandler(Filters.text, goodreads_books_in_tabadol_ketab_checker)],
        },
        fallbacks=[CommandHandler('cancel', cancel), CommandHandler('help', cancel), CommandHandler('start', cancel)],
    )

    search_multiple_books_converstation = ConversationHandler(
        entry_points=[CommandHandler('searchmultiplebooks', search_books_in_tabadol_ketab_intro)],
        states={
            GET_BOOKS_NAMES: [MessageHandler(Filters.text, search_multiple_books)],
        },
        fallbacks=[CommandHandler('cancel', cancel), CommandHandler('help', cancel), CommandHandler('start', cancel)],
    )

    dp.add_handler(goodreads_in_tabadolketab_converstation)
    dp.add_handler(search_multiple_books_converstation)
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(MessageHandler(Filters.text, search_a_book_by_only_name))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

