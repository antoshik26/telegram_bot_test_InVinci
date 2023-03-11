from telegram_bot.telegram_start import TelegramStart
from models.modelsmanager import model_fastncc

if __name__ == "__main__":
    '''
        В пременной token должен быть ваш токен сгенерированный в телеграмме BotFather
    '''
    token = ''
    model = model_fastncc(0.5, 'models_labels/test_importance.csv')
    telegram = TelegramStart(token, model)
    telegram.start_bot()
