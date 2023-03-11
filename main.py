from telegram_bot.telegram_start import TelegramStart
from models.modelsmanager import model_fastncc

if __name__ == "__main__":
    '''
        В пременной token должен быть ваш токен сгенерированный в телеграмме BotFather
    '''
    token = '5690057569:AAHNpVHJaylNch1Y7EAnWOq-s_pqfV-B1kk'
    model = model_fastncc(0.5, 'models_labels/test_importance.csv')
    telegram = TelegramStart(token, model)
    telegram.start_bot()
