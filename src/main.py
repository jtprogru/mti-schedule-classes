#!/usr/bin/env python3
import os
import sys

from telegram.ext import Application, CommandHandler

import bot


def main():
    token = os.getenv("BOT_TG_TOKEN", default='')
    if len(token) < 46:
        print("TOKEN IS NOT DEFINED!!!")
        sys.exit(1)
    print('token is defined')

    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token=token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", bot.start_command))
    application.add_handler(CommandHandler("help", bot.help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(CommandHandler("today", bot.today_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
