from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

import setting
from models import TabadolKetab

def main():
    updater = Updater(setting.telegram_access_token, use_context=True)
    dp = updater.dispatcher

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
