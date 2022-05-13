from random import choice
import telebot
from telebot import types

bot = telebot.TeleBot('5381048754:AAGPxknm4po_gLwRYTSBBDiCtLit4HWgdm8')

words = {'животные': ['жираф', 'слон', 'аллигатор', 'пчела', 'заяц', 'кролик', 'рысь', 'лиса', 'обезьяна', 'попугай',
                      'кот', 'собака', 'волк', 'страус', 'пингвин', 'ленивец', 'енот', 'мышь', 'крот', 'медведь',
                      'орёл', 'крыса',  'гусь', 'утка', 'лев', 'хорёк', 'ящерица', 'паук', 'варан', 'кузнечик'],
         'растения': ['кабачок', 'огурец', 'сукулент', 'яблоко', 'герань', 'орхидея', 'капуста', 'облепиха', 'дуб',
                      'кактус', 'сирень', 'сосна', 'папоротник', 'фикус', 'ель', 'кукруза', 'капуста',  'помидор'],
         'канцелярия': ['карандаш', 'ручка', 'ластик', 'точилка', 'пенал', 'циркуль', 'линейка', 'маркер', 'фломастер'],
         'мебель': ['стул', 'стол', 'табуретка', 'шкаф', 'полка', 'диван', 'кресло', 'подоконник', 'вешалка', 'кровать']}


def display_hangman(tries):
    stages = [  # финальное состояние: голова, торс, обе руки, обе ноги
                '''
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / \\
                   -
                ''',
                # голова, торс, обе руки, одна нога
                '''
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / 
                   -
                ''',
                # голова, торс, обе руки
                '''
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |      
                   -
                ''',
                # голова, торс и одна рука
                '''
                   --------
                   |      |
                   |      O
                   |     \\|
                   |      |
                   |     
                   -
                ''',
                # голова и торс
                '''
                   --------
                   |      |
                   |      O
                   |      |
                   |      |
                   |     
                   -
                ''',
                # голова
                '''
                   --------
                   |      |
                   |      O
                   |    
                   |      
                   |     
                   -
                ''',
                # начальное состояние
                '''
                   --------
                   |      |
                   |      
                   |    
                   |      
                   |     
                   -
                '''
    ]
    return stages[tries]


@bot.message_handler(commands=['guessing_game'])
def get_word(message):
    kb = types.InlineKeyboardMarkup(row_width=1)
    animals = types.InlineKeyboardButton(text='Животные', callback_data="животные")
    plants = types.InlineKeyboardButton(text='Растения', callback_data="растения")
    note = types.InlineKeyboardButton(text='Канцелярия', callback_data="канцелярия")
    tools = types.InlineKeyboardButton(text='Мебель', callback_data="мебель")
    kb.add(animals, plants, tools, note)
    bot.send_message(chat_id=message.chat.id, text='Давайте играть в угадайку слов!')
    bot.send_message(chat_id=message.chat.id, text='Выберите желаемую категорию:', reply_markup=kb)


@bot.callback_query_handler(func=lambda x: x.data in ['животные', 'растения', 'канцелярия', 'мебель'])
def topic(callback):
    word = choice(words[callback.data]).upper()
    main(callback.message, word)


def word_result(letters, word):
    flag = False
    word_completition = ''
    for i in word:
        for j in letters:
            if i.upper() == j.upper():
                word_completition += j.upper()
                flag = True
        if flag is False:
            word_completition += '_'
        flag = False
    return word_completition


def main(message, word):
    bot.send_message(chat_id=message.chat.id, text=f'Количество букв в слове: {len(word)}\n'
                                                   f'<b>{len(word) * "_"}</b>', parse_mode='HTML')
    kb = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    yes = types.KeyboardButton(text='Да')
    no = types.KeyboardButton(text='Нет')
    kb.add(yes, no)
    mes = bot.send_message(chat_id=message.chat.id, text='Хотите увидеть первую и последнюю буквы слова?', reply_markup=kb)
    bot.register_next_step_handler(mes, first, word)


def attempt(tries):
    if tries > 4:
        return 'попыток'
    elif tries > 1:
        return 'попытки'
    else:
        return 'попытка'


def first(message, word):
    tries = 6
    guessed_letters = ''
    if message.text == 'Да':
        guessed_letters = ''.join(set(word[0], word[-1]))
        bot.send_message(chat_id=message.chat.id, text=f'<b>{word_result(guessed_letters, word)}</b>', parse_mode='HTML')
    elif message.text == 'Нет':
        bot.send_message(chat_id=message.chat.id, text='Хорошо, тогда думайте своими мозгами...')
    bot.send_message(chat_id=message.chat.id, text=f'У вас есть всего 6 попыток, чтобы отгадать слово\n'
                                                   f'{display_hangman(tries)}')
    mes = bot.send_message(chat_id=message.chat.id, text='Введите букву')
    bot.register_next_step_handler(mes, enter, word, tries, guessed_letters)


def get_letter(message, word, tries, guessed_letters):
    mes = bot.send_message(chat_id=message.chat.id, text='Введите букву')
    bot.register_next_step_handler(mes, enter, word, tries, guessed_letters)


def enter(message, word, tries, guessed_letters):
    letter = message.text.lower()
    if letter in 'йцукенгшщзхъёфывапролджэячсмитьбю' and len(str(letter)) == 1:
        if letter.upper() in word and letter.upper() not in guessed_letters:
            guessed_letters += letter.upper()
            if word == word_result(guessed_letters, word):
                guess(message, word, tries, guessed_letters)
                return None
            bot.send_message(chat_id=message.chat.id, text=f'<b>{word_result(guessed_letters, word)}</b>', parse_mode='HTML')
            kb = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            yes = types.KeyboardButton(text='Да')
            no = types.KeyboardButton(text='Нет')
            kb.add(yes, no)
            mes = bot.send_message(chat_id=message.chat.id, text='Уже готовы угадать слово?', reply_markup=kb)
            bot.register_next_step_handler(mes, finish, word, tries, guessed_letters)
        else:
            bot.send_message(chat_id=message.chat.id, text='Этой буквы нет в слове')
            tries -= 1
            if tries == 0:
                bot.send_message(chat_id=message.chat.id, text='У вас закончились попытки и из-за вас повесили '
                                                               f'невинного человека\nА загаданное слово было "{word}"\n'
                                                               f'{display_hangman(tries)}\n\n'
                                                               f'Вы можете пропробовать переиграть '
                                                               'ситуацию и начать заново, введя команду /guessing_game '
                                                               'либо вернуться обратно, по команде /menu')
                return None
            bot.send_message(chat_id=message.chat.id, text=f'У вас осталось {tries} {attempt(tries)}\n{display_hangman(tries)}')
            get_letter(message, word, tries, guessed_letters)
    elif letter.upper() in guessed_letters:
        bot.send_message(chat_id=message.chat.id, text='Эта буква уже есть в слове, но так уж и быть, '
                                                       'не буду отнимать у вас попытку')
        get_letter(message, word, tries, guessed_letters)
    else:
        bot.send_message(chat_id=message.chat.id, text='Ваш символ не похож на русскую букву')
        get_letter(message, word, tries, guessed_letters)


def finish(message, word, tries, guessed_letters):
    if message.text == 'Да':
        mes = bot.send_message(chat_id=message.chat.id, text='Попробуйте угадать слово')
        bot.register_next_step_handler(mes, guess, word, tries, guessed_letters)
    else:
        tries -= 1
        bot.send_message(chat_id=message.chat.id, text='Хорошо, подбираем буквы дальше\n'
                                                       f'У вас осталось {tries} {attempt(tries)}\n{display_hangman(tries)}')
        get_letter(message, word, tries, guessed_letters)


def guess(message, word, tries, guessed_letters):
    kb = types.InlineKeyboardMarkup()
    openn = types.InlineKeyboardButton(text='Открыть!', callback_data='open')
    kb.add(openn)
    box = open('9BDE.gif', 'rb')
    if (message.text.upper() == word) or (word == word_result(guessed_letters, word)):
        bot.send_video(chat_id=message.chat.id, video=box)
        bot.send_message(chat_id=message.chat.id, text=f'Поздравляем! Вы отгадали слово {word} и получили таинственный приз\n'
                                                       'Откройте его и посмотрите, что же лежит внутри', reply_markup=kb)
    else:
        tries -= 1
        mes = bot.send_message(chat_id=message.chat.id, text='Увы, это неправильный ответ\n'
                                                             'Попробуйте отгадать ещё пару букв\n\n'
                                                             f'У вас осталось {tries} {attempt(tries)}\n'
                                                             f'{display_hangman(tries)}')
        get_letter(message, word, tries, guessed_letters)


@bot.callback_query_handler(func=lambda x: x.data == 'open')
def callback(callback):
    potato = open('70J.gif', 'rb')
    stickman = open('8BCj.gif', 'rb')
    bot.send_video(chat_id=callback.message.chat.id, video=potato)
    bot.send_message(chat_id=callback.message.chat.id, text='И это картошка с глазами!')
    bot.send_video(chat_id=callback.message.chat.id, video=stickman)
    bot.send_message(chat_id=callback.message.chat.id, text='И человечек на висилице, конечно, тоже остался жив')
    bot.send_message(chat_id=callback.message.chat.id, text='Ваша игра завершена, но если вам нехватило, '
                                                            'можете попробовать ещё разок, введя команду /guessing_game')


bot.polling()
