import logging
from telegram import Bot
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, filters


class telegrambot:
    '''
       Не стоит нашего внимания так как работает только с 1 пользователем
    '''
    def __init__(self, token):
        self.token = token
        self.updater, self.dispatcher = self.Update()

    def Update(self):
        bot = Bot(self.token)
        updater = Updater(bot, update_queue=0)
        dispatcher = updater.dispatcher
        return updater, dispatcher

    def logging(self):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

    def start_massage(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please give me a picture")

    def command_handler(self):
        start_handler = CommandHandler('start', self.start_massage)
        self.dispathrt.add_handler(start_handler)

    def start_polling(self):
        self.updater.start_polling()

    def ehco(self, context):
        text = 'ECHO: ' + self.updater.massage.text
        context.bot.send_message(chat_id=self.updater.effective_chat.id, text=text)

    def command_echo(self):
        echo_handler = MessageHandler(filters.text & (~filters.command), self.echo)
        self.dispatcher.add_handler(echo_handler)

    def caps(self, update, context):
        if (context.args):
            text_caps = ' '.join(context.args).upper()
            context.bot.send_message(chat_id=self.updater.effective_chat.id, text=text_caps)
        else:
            context.bot.send_message(chat_id=self.updater.effective_chat.id, text='No command argument')
            context.bot.send_message(chat_id=update.effective_chat.id, text='send: /caps argument')

    def caps_handler(self):
        caps_handler = CommandHandler('caps', self.caps)
        self.dispatcher.add_handler(caps_handler)

    def unknown_command(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Sorry, I didn't understand that command.")

    def unknown_raction(self):
        unknown_handler = MessageHandler(filters.command, self.unknown_command)
        self.dispatcher.add_handler(unknown_handler)
