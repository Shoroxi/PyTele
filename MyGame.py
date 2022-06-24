from telebot import types
import telebot
import random

import MenuBot
from MenuBot import Menu

bot = telebot.TeleBot(
    '5241329098:AAFwTwBMDbk8fD-GVHlXBlz52jI9X4SWoVk')


def goto_menu(chat_id, name_menu):
    # получение нужного элемента меню
    cur_menu = Menu.getCurMenu(chat_id)
    if name_menu == "Выход" and cur_menu is not None and cur_menu.parent is not None:
        Menu.getMenu(chat_id, cur_menu.parent.name)
    else:
        Menu.getMenu(chat_id, name_menu)


class Slots:
    players = []
    values = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
    call_list = ["Крутить", "Слоты", "Статистика", "Выход"]

    @property
    def flag(self):
        return self.__flag

    # Поток обработки сообщений
    @staticmethod
    def main_slots(call, bot):
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        button = []
        keyboard.add(*button)
        bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=keyboard, text="",
                              message_id=call.message.message_id)
        button.append(types.InlineKeyboardButton("Выход", callback_data='Выход'))
        button.append(types.InlineKeyboardButton("Крутить", callback_data='Крутить'))

    @classmethod
    def callback_inline(cls, call, bot, message):
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        button = []
        ms_text = message.text
        cls.__flag = True

        # Код при нажатии
        if call.data == 'Крутить' or ms_text == "Крутить":
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

            # Удаление inline-кнопки у предыдущего сообщения (остаётся только сообщение "Слоты: ")
            bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=None, text=call.message.text,
                                  message_id=call.message.message_id)

            # Подготовка inline-кнопок "Spin!" и "Exit" к следующему сообщению
            keyboard = types.InlineKeyboardMarkup(row_width=3)
            b1 = button.append(types.InlineKeyboardButton("Крутить", callback_data='Крутить'))
            b2 = button.append(types.InlineKeyboardButton("Выход", callback_data='Выход'))
            keyboard.add(b1, b2)

            # Крепление inline-меню (кнопки "Spin!" и "Exit") и вывод слотов пользователю

            bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=keyboard,
                                  text="{}\n{}{}{}\n{}{}{}\n{}{}{}".format(*new_array),
                                  message_id=call.message.message_id)

            # Проверка выигрыша (на данный момент просто проверка всех строк и столбцов)
            # При удовлетворении условию выводится уведомление с поздравлением
            if new_array[0] == new_array[1] == new_array[2] or new_array[3] == new_array[4] == new_array[5] or \
                    new_array[6] == new_array[7] == new_array[8] or new_array[0] == new_array[3] == new_array[6] or \
                    new_array[1] == new_array[4] == new_array[7] or new_array[2] == new_array[5] == new_array[8]:
                bot.answer_callback_query(callback_query_id=call.id, text="Jackpot!!!", show_alert=True)


def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Слоты" or message.text == 'Крутить':
        Slots.callback_inline(message, bot)
    elif ms_text == "Выход":
        MenuBot.goto_menu(bot, chat_id, "Главное меню")

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call, message, cls):
    chat_d = call.message.chat.id
    m_text = message.text
    if call.data == "Слоты" or call.data == "Крутить":
        cls.main_slots(call, bot)
        Slots.callback_inline(chat_d, bot)
        return
