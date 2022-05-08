import telebot
from telebot import types
import random
import re

bot = telebot.TeleBot('5381048754:AAGPxknm4po_gLwRYTSBBDiCtLit4HWgdm8')

# главное меню
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, text='<b>Вот небольшой список команд, '
                                           'с помощью которых ты можешь увидеть все мои возможности:\n\n</b>'
                                           '📍 Для того, что болучить секретную информацию, отправь команду /getsecretinfo\n'
                                           '📍 Если хочешь немного узнать о любимых треках скромнейшего '
                                           'создателя этого бота, отправь команду /get_tracks\n'
                                           '📍 Чтобы увидеть демо-меню потенциального ресторанчика, отправь команду /chum\n'
                                           '📍 Если же тебя инетересует покупка уникальных цифровых товаров, отправь команду /store\n'
                                           '📍 Биткойн можно купить, введя команду /btc\n'
                                           '📍 Если вам везапно понадобилось решить квадратное уравнение, '
                                           'введите команду /equation\n'
                                           '📍 Услуги магического шара предоставляются по команде /magic_ball',
                                            parse_mode='HTML')
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton(text='/menu', )
    kb.add(back)
    bot.send_message(message.chat.id, text=' В любой  непонятной ситуации вводи команду /menu либо жми на кнопку внизу',
                     reply_markup=kb)


@bot.message_handler(commands=['menu'])
def menu(message):
    start(message)


@bot.message_handler(commands=['getsecretinfo'])
def rickroll(message):
    kb = types.InlineKeyboardMarkup()
    link = types.InlineKeyboardButton(text='Секретная информация', url='https://www.youtube.com/watch?v=FuJM-90oMvo')
    kb.add(link)
    bot.send_message(message.chat.id, text='Перейди по ссылке, чтобы получить секретную информацию', reply_markup=kb)


# любимые и нелюбимые песни через inline callback и url кнопки
@bot.message_handler(commands=['get_tracks'])
def get_tracks(message):
    kb = types.InlineKeyboardMarkup(row_width=2)
    love = types.InlineKeyboardButton(text='Мои любимые треки!', callback_data='love')
    hate = types.InlineKeyboardButton(text='Ненавижу эти треки!', callback_data='hate')
    kb.add(love, hate)
    bot.send_message(message.chat.id, text='Выбери, что тебе нужно:', reply_markup=kb)


@bot.callback_query_handler(func=lambda x: x.data in ['love', 'hate'])
def callback(callback):
    kb = types.InlineKeyboardMarkup(row_width=1)
    if callback.data == 'love':
        shrek = types.InlineKeyboardButton(text='Shreksophone 10 hours', url='https://www.youtube.com/watch?v=pxw-5qfJ1dk')
        hoiser = types.InlineKeyboardButton(text='Take me to church', url='https://www.youtube.com/watch?v=PVjiKRfKpPI')
        grieg = types.InlineKeyboardButton(text='In the Hall of the Mountain King by genius Deniska',
                                           url='https://www.youtube.com/watch?v=0nZhw3wifeY')
        kb.add(shrek, hoiser, grieg)
        bot.send_message(callback.message.chat.id, text='Чтобы вернуться в начало, опять введите /get_tracks. '
                                                        'Вот мои любимые треки:', reply_markup=kb)
    else:
        buzova = types.InlineKeyboardButton(text='Олечка Бузова', url='https://www.youtube.com/watch?v=gUGu0F02p9Y')
        kb.add(buzova)
        bot.send_message(callback.message.chat.id, text='Чтобы вернуться в начало, введите /get_tracks. '
                                                        'Вот песня, которая мне не нравится:', reply_markup=kb)


# многократное изменение сообщений
@bot.message_handler(commands=['chum'])
def chum(message):
    kb = types.InlineKeyboardMarkup()
    menu = types.InlineKeyboardButton(text='Меню', callback_data='menu')
    kb.add(menu)
    bot.send_message(message.chat.id, text='Добро пожаловать в ресторан Chum Bucket!', reply_markup=kb)


@bot.callback_query_handler(func=lambda x: x.data in ['menu', 'wat', 'again'])
def callback(callback):
    kb = types.InlineKeyboardMarkup()
    if callback.data == 'menu':
        water = types.InlineKeyboardButton(text='Вода', callback_data='wat')
        back = types.InlineKeyboardButton(text='Назад', callback_data='again')
        kb.add(water, back)
        bot.edit_message_text(chat_id=callback.message.chat.id, text='Вот наше меню',
                              reply_markup=kb, message_id=callback.message.message_id)
    elif callback.data == 'wat':
        back = types.InlineKeyboardButton(text='Вернуться в меню', callback_data='menu')
        kb.add(back)
        bot.edit_message_text(chat_id=callback.message.chat.id, text='Простите, воды нет, мы банкроты',
                              reply_markup=kb, message_id=callback.message.message_id)
    elif callback.data == 'again':
        menu = types.InlineKeyboardButton(text='Меню', callback_data='menu')
        kb.add(menu)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                              text='Добро пожаловать в ресторан Chum Bucket!', reply_markup=kb)


# Работа с клавиатурой, "Интренет-магазин"
@bot.message_handler(commands=['store'])
def store(message):
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    buy = types.KeyboardButton(text="Купить🎁")
    kb.add(buy)
    bot.send_message(message.chat.id, text='Добро пожаловать в интернет-магазин', reply_markup=kb)


@bot.message_handler(func=lambda message: message.text in ['Купить🎁', 'Камень с глазами', 'Назад'])
def buy(message):
    if message.text == 'Купить🎁':
        kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        stone = types.KeyboardButton(text='Камень с глазами')
        back = types.KeyboardButton(text='Назад')
        kb.add(stone, back)
        bot.send_message(message.chat.id, text='Что хотите купить?', reply_markup=kb)
    elif message.text == 'Камень с глазами':
        photo = open('Pete_the_rock.png', 'rb')
        bot.send_photo(message.chat.id, photo, 'Товар: камень с глазами\n'
                                               'Цена: 1000$\n'
                                               'В наличии: 2')
        bot.send_message(message.chat.id, text="Чтобы вернуться назад, введите команду /store")
    else:
        store(message)


# редактирование сообщения
@bot.message_handler(commands=['btc'])
def fraud(message):
    bot.send_message(message.chat.id, 'Хотите купить биткоин?\nПишите "/buy"')


@bot.message_handler(commands=['buy'])
def buy(message):
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id-1, text='Хотите купить свежайшего барана?')
    bot.send_message(message.chat.id, 'Сколько кило?')


# магический шар
@bot.message_handler(commands=['magic_ball'])
def magic_ball(message):
    bot.send_message(message.chat.id, text='Привет Мир, я магический шар, и я знаю ответ на любой вопрос.')

    send = bot.send_message(message.chat.id, text='Задай свой вопрос')
    bot.register_next_step_handler(send, return_answer)


def return_answer(message):
    answers = ['Бесспорно', 'Мне кажется - да', 'Пока неясно, попробуй снова', 'Даже не думай', 'Предрешено',
               'Вероятнее всего', 'Спроси позже', 'Мой ответ - нет', 'Никаких сомнений', 'Хорошие перспективы',
               'Лучше не рассказывать', 'По моим данным - нет', 'Определённо да', 'Знаки говорят - да',
               'Сейчас нельзя предсказать', 'Перспективы не очень хорошие', 'Можешь быть уверен в этом', 'Да',
               'Весьма сомнительно']

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    yes = types.KeyboardButton(text='Да')
    no = types.KeyboardButton(text='Нет')
    kb.add(yes, no)

    if message.text == 'Нет':
        bot.send_message(chat_id=message.chat.id, text='Возвращайся, если возникнут вопросы!')
    elif message.text == 'Да':
        send = bot.send_message(message.chat.id, text='Задай свой вопрос')
        bot.register_next_step_handler(send, return_answer)
    else:
        bot.send_message(message.chat.id, text=f'{random.choice(answers)}')
        ans = bot.send_message(message.chat.id, text='Остались ещё вопросы?', reply_markup=kb)
        bot.register_next_step_handler(ans, return_answer)


# решение квадратных уравнений
@bot.message_handler(commands=['equation'])
def equ(message):
    kb = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button = types.KeyboardButton('Решить квадратное уравнение')
    kb.add(button)
    bot.send_message(chat_id=message.chat.id, text='Привет, что тебя интересует?', reply_markup=kb)


@bot.message_handler(func=lambda x: x.text == 'Решить квадратное уравнение')
def equation(message):
    mes = bot.send_message(chat_id=message.chat.id, text='Введите коэффиценты ax^2 + bx + c '
                                                         'в виде a b c\nПример: 1 -2 5')
    bot.register_next_step_handler(mes, proc)


def proc(message):
    if re.fullmatch(r'[-+]?\d+ [-+]?\d+ [-+]?\d+', message.text):
        bot.send_message(chat_id=message.chat.id, text='Всё введено верно. Начинаю решать уравнение')
        a, b, c = map(int, message.text.split(' '))
        d = b ** 2 - (4 * a * c)
        bot.send_message(chat_id=message.chat.id, text=f'Дискриминант уравнения: {d}')
        if d < 0:
            bot.send_message(chat_id=message.chat.id, text='У уравнения нет корней')
        elif d == 0:
            bot.send_message(chat_id=message.chat.id, text=f'У уравнения 1 корень: {-b / (2 * a)}')
        else:
            bot.send_message(chat_id=message.chat.id, text=f'У уравнения 2 кореня\nпервый корень: {(-b - d) / (2 * a)}\n'
                                                           f'второй корень: {(-b + d) / (2 * a)}')

    else:
        mes = bot.send_message(chat_id=message.chat.id, text='Данные введены некорректно, попробуйте ещё раз')
        bot.register_next_step_handler(mes, proc)


bot.polling()
