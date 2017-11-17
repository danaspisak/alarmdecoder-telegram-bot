#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

import sys
import telnetlib
import time
import threading

import ConfigParser

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

HOST = "localhost"
PORT = 10000
TAIL_LEN = 4

message_tail = []
to_send = []
id = ""


class TelnetReader(threading.Thread):
    def __init__(self):
        super(TelnetReader, self).__init__()
        self.tn = telnetlib.Telnet(HOST,PORT)
        message_tail = []

    def run(self):
        while True:
            response = self.tn.read_until("\n",0.1)
            if response:
              response_list = response.split(',')
              if len(response_list) == 4:
                  message = response_list[3]
                  if len(message_tail) == TAIL_LEN:
                      message_tail.pop(0)
                  message_tail.append(message)
            time.sleep(1)
            while len(to_send):
                command = to_send.pop(0)
                print command
                self.tn.write(command)



# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    global id
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')
    chat_id = update.message.chat_id
    print chat_id
    print id
    if chat_id == id:
        update.message.reply_text("Hello ;)")


def tail(bot, update):
    chat_id = update.message.chat_id
    if chat_id == id:
        update.message.reply_text("".join(message_tail))
        

def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('/panel <CODE>+COMMAND')
    layout = ["1 - OFF",
              "2 - AWAY",
              "3 - STAY",
              "4 - MAX",
              "5 - TEST",
              "6 - BYPASS",
              "7 - INSTANT",
              "8 - CODE",
              "9 - CHIME",
              "* - READY"]
    update.message.reply_text("\r\n".join(layout))

def panel(bot, update):
    chat_id = update.message.chat_id
    if chat_id == id:
      str = update.message.text.replace("/panel ", "")
      to_send.append(str.encode('utf-8'))

def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    global id

    print "-=#!!! This is terribly insecure !!!#=-"
    print "   !!! Add some mechanism to     !!!"
    print "   !!! verify the chat user.     !!!"
    config = ConfigParser.ConfigParser()
    config.read("./.config")
    token = config.get("configuration","token")
    id = int(config.get("configuration","id"))

    tr = TelnetReader()
    tr.daemon = True
    tr.start()

    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("tail", tail))
    dp.add_handler(CommandHandler("panel", panel))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
