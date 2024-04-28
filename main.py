import telebot
from PIL import Image
import numpy as np
from model import model


bot = telebot.TeleBot('7179107261:AAGu16cquR18pVn_5D87dV-j1WNmdJ484jg')

name = ''

CLASSES = {
    0: 'футболка',
    1: 'шорты',
    2: 'свитер',
    3: 'платье',
    4: 'плащ',
    5: 'санадали',
    6: 'рубашка',
    7: 'кроссовки',
    8: 'сумка',
    9: 'ботинки',
}


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, 'Привет!')
    bot.send_message(message.from_user.id, 'Как тебя зовут?')
    bot.register_next_step_handler(message, get_name)


@bot.message_handler(content_types=['photo'])
def predict_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)

    image = Image.open('image.jpg')
    image = image.resize((28, 28))
    image = image.convert("L")
    image = np.array(image)
    image = image.reshape(-1, 28, 28, 1)

    predictions = model.predict(image)
    predict = np.argmax(predictions, axis=1)
    bot.send_message(message.from_user.id, f'Я считаю это - {CLASSES[predict[0]]}')


@bot.message_handler(content_types=['text'])
def answer(message):
    bot.send_message(message.from_user.id,
                     f'Я бот определяющий по картинке одежду: футболку, шорты, свитер, платье, плащ, санадали, рубашку, кроссовки, сумку, ботинки.')
    bot.send_message(message.from_user.id, f'Отправьте мне картинку')


def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, f'Приятно познакомиться, {name}!')
    bot.send_message(message.from_user.id, f'Я бот определяющий по картинке одежду: футболку, шорты, свитер, платье, плащ, санадали, рубашку, кроссовки, сумку, ботинки.')
    bot.send_message(message.from_user.id, f'Отправьте мне картинку')


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)