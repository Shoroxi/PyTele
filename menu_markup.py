"""
Клавиатура главного меню.
"""
from telebot import types, TeleBot
from translation import Translation

bot = TeleBot(
    '5494054794:AAG4jIdW1E5k4IaNIv5-LdZw9KhJR8o0-6g')

def gen_menu_keyboard(user_id, chat_type):
    """
    Функция генерации клавиатуры главного меню.

    :param user_id: ID пользователя.
    :param chat_type: Тип чата.
    :return: Клавиатура.
    """
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    menu_buttons = [types.ReplyKeyboardMarkup(resize_keyboard=True)]
    text = Translation.get_menu_expression(key="Slots", user_id=user_id)
    bot.send_message(user_id, text)
    #
    # if chat_type[0:7] == "private":
    #     menu_buttons.extend([types.ReplyKeyboardMarkup(callback_data="XO_start"), types.ReplyKeyboardMarkup(callback_data="Dating_start")])
    #     text = Translation.get_menu_expression(key="dating", user_id=user_id)
    #     bot.send_message(user_id, text)
    #
    # else:
    #     menu_buttons.append(types.ReplyKeyboardMarkup(callback_data="XO_group"))
    #     text = Translation.get_menu_expression(key="XO_private", user_id=user_id)
    #     bot.send_message(user_id, text)

    menu_buttons.append(types.ReplyKeyboardMarkup(resize_keyboard=True))
    text = Translation.get_menu_expression(key="language", user_id=user_id)
    bot.send_message(user_id, text)

    keyboard.add(*menu_buttons)
    return keyboard