import io
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.ext import MessageHandler, filters


class async_telegram_bot():
    def __init__(self, token, detector):
        '''
            Это конструктор.
            Принимает на себы 2 параметра:
            1. token полученый от BotFather telegram
            2. detector который будет использоваться при разборе картинок
        '''
        self.token = token
        self.detector = detector
        self.application = self.application_bot()

    def Update(self):
        '''
            Не Используетвся
        '''
        update = Update(token=self.token, use_contex=True)
        dispatcher = update.dispatcher
        return update, dispatcher

    def application_bot(self):
        '''
            Создание бота
        '''
        application = ApplicationBuilder().token(self.token).build()
        return application

    async def start(self, update, context):
        '''
            команда start
        '''
        await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please give me a picture!")

    def command_handler(self):
        '''
            Описание команды start для бота
        '''
        start_handler = CommandHandler('start', self.start)
        self.application.add_handler(start_handler)

    async def get_file(self, update, context):
        '''
            Основная функция которая обрабатывает картинки
        '''
        try:
            if (update.message is not None):
                message = update.message
            else:
                message = update.callback_query.massage
            file_id = update.message.photo[0].file_id
            new_file = await context.bot.get_file(file_id)
            if (new_file.file_path.lower().endswith(('.png', '.bmp', '.jpeg'))):
                await context.bot.send_message(chat_id=update.effective_chat.id,text='Файл не того расширения! Нужно png, bmp или jpeg')
                raise Exception("Файл не того расширения")
            #await new_file.download('test.png')
            #new_file_2 = self.detector.resize_image('..//test.png')
            predict_photo, rezult_new_file_2 = self.detector.predict(new_file.file_path)
            await update.message.reply_text("Image received")
            #raw = message.photo[2].fileid
            #path = raw+".jpg"
            #image = cv2.imread('C:\\Users\\gomez\\Desktop\\11.png', cv2.IMREAD_UNCHANGED)
            #await message.reply_photo(photo=open('C:\\Users\\gomez\\Desktop\\11.png', 'rb'), caption="результат детектора")
            #print(type(rezult_new_file_2))
            #rezult_new_file_2.save('img1.jpg')
            #a = open('img1.jpeg', 'rb')
            #print(a)
            output = io.BytesIO()
            rezult_new_file_2.save(output, format='JPEG')
            hex_data = output.getvalue()
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=hex_data, caption="результат детектора")
            str_predict = ''
            j = 0
            #print(predict_photo)
            lsit_predict_labels = {}
            for i in predict_photo[0]['scores'].tolist():
                if i > self.detector.predict_scores_threshold:
                    name_labels = predict_photo[0]["labels"].tolist()[j]
                    lsit_predict_labels[self.detector.labels.values[name_labels][0]] = [self.detector.labels.values[name_labels][1], i]
                    j += 1
            sorted_list_predict_photo = {k: v for k, v in sorted(lsit_predict_labels.items(), key=lambda item: item[1][0])}
            for k, v in sorted_list_predict_photo.items():
                str_predict = str_predict + f'label = {k}, score = {v[1]}\n'
            if len(str_predict) == 0:
                await context.bot.send_message(chat_id=update.effective_chat.id, text='Не нашел ничего что бы привлекло внимание детектор.')
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=str_predict)
        except ValueError:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='что то пошло не так попытайтесь попозже')

    def return_file(self):
        '''
            Описание команды return_file для бота
        '''
        photo_handler = MessageHandler(filters.PHOTO, self.get_file)
        self.application.add_handler(photo_handler)

    async def echo(self, update, context):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

    def command_echo(self):
        '''
            Просто возвращает вест=ь бред написнаый пользователем
        '''
        echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), self.echo)
        self.application.add_handler(echo_handler)

    async def caps(self, update, context):
        text_caps = ' '.join(context.args).upper()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

    def caps_handler(self):
        '''
            Просто возвращает вест=ь бред написнаый пользователем БОЛЬШИМИ БУКВАМИ
        '''
        caps_handler = CommandHandler('caps', self.caps)
        self.application.add_handler(caps_handler)

    async def unknown_command(self, update, context):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

    def unknown_raction(self):
        '''
            Обработчик неизвестных нам команд
        '''
        unknown_handler = MessageHandler(filters.COMMAND, self.unknown_command)
        self.application.add_handler(unknown_handler)

    def start_polling(self):
        '''
            запуск бота stop_signals=None параметр потому что пишу я его на windows
            На маке этот пораметр stop_signals=None нужен
        '''
        self.application.run_polling(stop_signals=None)
