import telebot as tb
import json
import random as ran


token = "8029162780:AAGvTWVtQrzQoQQCzwLc1sDujxgRIRwJ4eM"

bot = tb.TeleBot(token)

with open("user_dictionary.json", "r", encoding="utf-8") as f:
    user_data = json.load(f)

@bot.message_handler(commands=["start"])
def start(message):
    name = message.from_user.first_name
    bot.send_message(message.chat.id, f"Hello {name}!")

@bot.message_handler(commands=["learn"])
def learn(message):
    word_list = user_data.get(str(message.chat.id), {})
    try:
        words_number = int(message.text.split()[1])
        ask_translation(message.chat.id, word_list, words_number)
    except IndexError:
        bot.send_message(message.chat.id, "Прозашла ошибка. Вы не написали после '/learn' число. Пример: /learn 2")
    except ValueError:
        bot.send_message(message.chat.id, "Произашла ошибка. Вы после '/learn' написали НЕ число. Пример: /learn 2")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произашла ошибка: {e}")
    

def ask_translation(chat_id, user_words, words_left):
    if words_left > 0:
        word = ran.choice(list(user_words.keys()))
        translation = user_words[word]
        bot.send_message(chat_id, f"Напиши перевод слова {word}.")
        bot.register_next_step_handler_by_chat_id(chat_id, check_translation, translation, words_left)
    else:
        bot.send_message(chat_id, "Урок закончен!")

def check_translation(message, expected_translation, words_left):
    user_translation = message.text.strip().lower()
    if user_translation.lower() == expected_translation.lower():
        bot.send_message(message.chat.id, "Правильно, Молодец!")
    else:
        bot.send_message(message.chat.id, f"Неверно. Правильный перевод: {expected_translation}")

    ask_translation(message.chat.id, user_data[str(message.chat.id)], words_left-1)

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, "Здрасpтвуйте. Я бот для изучения анлийского языка. \nУ меня пока есть 2 комманды.\n/addword - Добавляет слово в ваш сдоварь. Пример: /addword яблоко apple\n/learn - комманда для начала обучения слов из вашего словаря.\nАвтор: Вова Ушаков, 10 лет, студент курса python-разработки в Skysmart ")

@bot.message_handler(commands=["addword"])
def add_word(message):
    global user_data
    chat_id = message.chat.id
    user_dict = user_data.get(chat_id, {})
    try:
        words = message.text.split()[1:]
        if len(words) == 2:
            word, translation = words[0].lower(), words[1].lower()
            user_dict[word] = translation
            user_data[chat_id] = user_dict
            with open("user_dictionary.json", "w", encoding="utf-8") as file:
                json.dump(user_data, file, ensure_ascii=False, indent=4)
            bot.send_message(chat_id, f"Слово {word} добавлено в словарь")
        else:
            bot.send_message(chat_id, "Произошла ошибка. Надо после /addword написать 2 слова. Пример: /addword яблоко apple.")
    except Exception as e:
        bot.send_message(chat_id, f"Произошла ошибка: {e}")



@bot.message_handler(func=lambda message: True)
def handle_all(message):
    if message.text.lower() == "как тебя зовут?":
        bot.send_message(message.chat.id, "Я Vova_Json!")
    elif message.text.lower() not in ["как тебя зовут?"]:
        if message.text.lower()[0] == "/":
            bot.send_message(message.chat.id, "Я не знаю такую комманду.")
        else:
            bot.send_message(message.chat.id, "Чё?")

bot.polling(none_stop=True)