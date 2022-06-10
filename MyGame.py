from telebot import types
import telebot
import random
import MenuBot
from MenuBot import Menu

bot = telebot.TeleBot(
    '5241329098:AAFwTwBMDbk8fD-GVHlXBlz52jI9X4SWoVk')


def goto_menu(bot, chat_id, name_menu):
    # получение нужного элемента меню
    cur_menu = Menu.getCurMenu(chat_id)
    if name_menu == "Выход" and cur_menu != None and cur_menu.parent != None:
        target_menu = Menu.getMenu(chat_id, cur_menu.parent.name)
    else:
        target_menu = Menu.getMenu(chat_id, name_menu)


class Slots:
    @property
    def flag(self):
        return self.__flag

    # Поток обработки сообщений
    @staticmethod
    def main_Slots(message, bot):

        markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        button_list = ['Крутить']
        markup.add(*button_list)
        bot.send_message(message.from_user.id, text="Вернулись в главное меню", reply_markup=markup)

    @classmethod
    def callback_inline(cls, message, bot):
        cls.__flag = True

        if message.text == "Слоты":
            cls.main_Slots(message, bot)
            return

        if message.text == 'Крутить':
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
            button_list = ['Крутить', "Выход"]
            markup.add(*button_list)

            # Крепление inline-меню (кнопки "Крутить!" и "Exit") и вывод слотов пользователю

            bot.send_message(message.from_user.id, text="\n{}{}{}\n{}{}{}\n{}{}{}".format(*new_array),
                             reply_markup=markup)

            # При удовлетворении условию выводится уведомление с поздравлением
            if new_array[0] == new_array[1] == new_array[2] or new_array[3] == new_array[4] == new_array[5] or \
                    new_array[6] == new_array[7] == new_array[8] or new_array[0] == new_array[3] == new_array[6] or \
                    new_array[1] == new_array[4] == new_array[7] or new_array[2] == new_array[5] == new_array[8]:
                bot.send_message(message.chat.id, text="Джекпот!!!")


def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Слоты" or message.text == 'Крутить':
        Slots.callback_inline(message, bot)
    elif ms_text == "Выход":
        MenuBot.goto_menu(bot, chat_id, "Главное меню")