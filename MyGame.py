from telebot import types
import telebot
import random
from MenuBot import goto_menu
import json

from menu_markup import gen_menu_keyboard
from translation import Translation


bot = telebot.TeleBot(
    '5241329098:AAFwTwBMDbk8fD-GVHlXBlz52jI9X4SWoVk')


class Slots:
    @property
    def flag(self):
        return self.__flag

    # Поток обработки сообщений
    @staticmethod
    def main_slots(message, bot):

        markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        b = types.ReplyKeyboardMarkup(Translation.get_slots_menu_expression("spin", message.from_user.id))
        button_list = ['spin']
        markup.add(*button_list)
        bot.send_message(message.from_user.id, text="Вернулись в главное меню", reply_markup=markup)

    @classmethod
    def callback_inline(cls, message, bot):
        cls.__flag = True

        if message.text == "Slots":
            cls.main_slots(message, bot)
            return

        if message.text == 'spin':
            i = 0
            array = []

            # Генерация случайного списка, от которого зависит выигрыш
            while i < 9:
                array.append(random.randint(0, 4))
                i = i + 1
            new_array = []
            i = 0

            # Замена случайных чисел на картинки для наглядности
            while i < 9:
                if array[i] == 0:
                    new_array.append("7️⃣")
                elif array[i] == 1:
                    new_array.append("🍒")
                elif array[i] == 2:
                    new_array.append("🍋")
                elif array[i] == 3:
                    new_array.append("🍎")
                elif array[i] == 4:
                    new_array.append("🍉")
                i += 1

            markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
            button_list = ['spin', "Выход"]
            markup.add(*button_list)

            # Крепление inline-меню (кнопки "Spin!" и "Exit") и вывод слотов пользователю
            message_string = Translation.get_slots_menu_expression("output", message.from_user.id)

            bot.send_message(message.from_user.id, text="{}\n{}{}{}\n{}{}{}\n{}{}{}".format(message_string, *new_array), reply_markup=markup)

            # При удовлетворении условию выводится уведомление с поздравлением
            if new_array[0] == new_array[1] == new_array[2] or new_array[3] == new_array[4] == new_array[5] or \
                    new_array[6] == new_array[7] == new_array[8] or new_array[0] == new_array[3] == new_array[6] or \
                    new_array[1] == new_array[4] == new_array[7] or new_array[2] == new_array[5] == new_array[8]:
                bot.answer_callback_query(callback_query_id=message.id, text="Jackpot!!!", show_alert=True)

def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Menu":
        bot.edit_message_text(chat_id=chat_id,
                              reply_markup=gen_menu_keyboard(message.from_user.id, message.chat.type),
                              text=Translation.get_menu_expression(key="choose_game", user_id=message.from_user.id),
                              message_id=message.message_id)

    elif ms_text == "language":
        Translation.switch_language(message.from_user.id)
        bot.edit_message_text(chat_id=chat_id,
                              reply_markup=gen_menu_keyboard(message.from_user.id, message.message.chat.type),
                              text=Translation.get_menu_expression(key="choose_game", user_id=message.from_user.id),
                              message_id=message.message_id)

    elif ms_text == "Slots" or message.text == 'spin':
        Slots.callback_inline(message, bot)
