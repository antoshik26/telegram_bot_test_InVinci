from telegram_bot.teltgrammanager import telegrambot
from telegram_bot.asinc_bot import async_telegram_bot


class TelegramStart(async_telegram_bot):
    def __init__(self, token, detector):
        '''
            Конструктор запускает инизиализацию конструктора наследуемого класса
        '''
        super().__init__(token, detector)

    def start_bot(self):
        '''
            Определение функция бота и запуск его
        '''
        self.return_file()
        self.command_handler()
        self.command_echo()
        self.caps_handler()
        self.unknown_raction()
        self.start_polling()
