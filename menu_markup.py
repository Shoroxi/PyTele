
from telebot import types, TeleBot
from translation import Translation

bot = TeleBot(
    '5241329098:AAFwTwBMDbk8fD-GVHlXBlz52jI9X4SWoVk')

def gen_menu_keyboard(user_id, chat_type):
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    menu_buttons = [types.ReplyKeyboardMarkup(resize_keyboard=True)]
    text = Translation.get_menu_expression(key="Slots", user_id=user_id)
    bot.send_message(user_id, text)

    menu_buttons.append(types.ReplyKeyboardMarkup(resize_keyboard=True))
    text = Translation.get_menu_expression(key="language", user_id=user_id)
    bot.send_message(user_id, text)

    keyboard.add(*menu_buttons)
    return keyboard