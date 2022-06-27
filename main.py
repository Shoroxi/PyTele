# Телеграм-бот v. 002 - Меню
try:
    from telebot import types
    import telebot
except ImportError:
    print("Не импортнул бота")

import MenuBot
from MenuBot import Menu
import Games
import DZ
import FUN
from FUN import get_dog, get_anekdot
import MyGame


bot = telebot.TeleBot('5241329098:AAFwTwBMDbk8fD-GVHlXBlz52jI9X4SWoVk')


# t.me/Artem_Boyarchenko_1MD4_bot # Создаем экземпляр бота @Artem_Boyarchenko_1MD4_bot


# -----------------------------------------------------------------------
# Функция, обрабатывающая команду
@bot.message_handler(commands=["start"])
def start(message, res=False):
    chat_id = message.chat.id

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Главное меню")
    btn2 = types.KeyboardButton("Помощь")
    markup.add(btn1, btn2)
    bot.send_message(chat_id,
                     text="Привет, {0.first_name}! Я тестовый бот для курса программирования на языке Пайтон".format(
                         message.from_user), reply_markup=markup)


# Получение сообщений от юзера
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    ms_text = message.text

    cur_user = MenuBot.Users.getUser(chat_id)
    if cur_user is None:
        cur_user = MenuBot.Users(chat_id, message.json["from"])

    # проверка = мы нажали кнопку подменю, или кнопку действия
    subMenu = MenuBot.goto_menu(bot, chat_id, ms_text)  # попытаемся использовать текст как команду меню, и войти в него
    if subMenu is not None:
        # Проверим, нет ли обработчика для самого меню. Если есть - выполним нужные команды
        if subMenu.name == "Игра в 21":
            game21 = Games.newgame(chat_id, Games.Game21(jokers_enabled=True))  # создаём новый экземпляр игры
            text_game = game21.get_cards(2)  # просим 2 карты в начале игры
            bot.send_media_group(chat_id, media=game21.mediaCards)  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

        elif subMenu.name == "Игра КНБ":
            GameRPS = Games.newgame(chat_id, Games.RPS())  # создаём новый экземпляр игры и регистрируем его
            bot.send_photo(caption=GameRPS.text_rules, parse_mode='HTML')

        return  # мы вошли в под-меню, и дальнейшая обработка не требуется

    # проверим, является ли текст текущий команды кнопкой действия
    cur_menu = Menu.getCurMenu(chat_id)
    if cur_menu is not None and ms_text in cur_menu.buttons:  # проверим, что команда относится к текущему меню
        module = cur_menu.module

        if module != "":  # принцип инкапсуляции
            exec(module + ".get_text_messages(bot, cur_user, message)")

    else:  # ======================================= случайный текст
        bot.send_message(chat_id, text="Мне жаль, я не понимаю вашу команду: " + ms_text)
        MenuBot.goto_menu(bot, chat_id, "Главное меню")


# -----------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    chat_id = call.message.chat.id
    cur_user = MenuBot.Users.getUser(chat_id)
    if cur_user is None:
        cur_user = MenuBot.Users(chat_id, call.message.json["from"])

    tmp = call.data.split("|")
    menu = tmp[0] if len(tmp) > 0 else ""
    cmd = tmp[1] if len(tmp) > 1 else ""
    par = tmp[2] if len(tmp) > 2 else ""

    if menu == "Игра К-Н-Б":
        Games.callback_worker(bot, cur_user, cmd, par, call)  # обработчик кнопок игры находится в модули игры


# -----------------------------------------------------------------------
# Модули запросов
def MediaCards(game21):
    medias = []
    for url in game21.arr_cards_URL:
        medias.append(types.InputMediaPhoto(url))
    return medias

def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Прислать собаку":
        bot.send_message(chat_id, get_dog())

    elif ms_text == "Прислать анекдот":
        bot.send_message(chat_id, text=get_anekdot())

    elif ms_text == "Помощь":
        help(bot, chat_id)

# -----------------------------------------------------------------------

bot.polling(none_stop=True, interval=0)  # Запускаем бота
