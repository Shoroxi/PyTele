# ======================================= Развлечения
import bs4
import requests
import re
from telebot import types
import MenuBot

def help(bot, chat_id):
    bot.send_message(chat_id, "Автор: Боярченко Артём")
    key1 = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Напишите автору", url="https://t.me/ArtemBoyarch")  # Ссылка на себя
    key1.add(btn1)
    img = open('i6lASX19BOY.jpg', 'rb')
    bot.send_photo(chat_id, img, reply_markup=key1)

    bot.send_message(chat_id, "Активные пользователи чат-бота:")
    for el in MenuBot.Users.activeUsers:
        bot.send_message(chat_id, MenuBot.Users.activeUsers[el].getUserHTML(), parse_mode='HTML')

# -----------------------------------------------------------------------
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
def get_dog():  # Cсылки на картиночки собак
    global url
    contents = requests.get('https://random.dog/woof.json').json()
    image_url = contents['url']
    allowed_extension = ['jpg', 'jpeg', 'png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = image_url
        file_extension = re.search("([^.]*)$", url).group(1).lower()
    return url


def get_anekdot():  # Анекдоты (Проблема с модулем)
    array_anekdots = []
    req_anek = requests.get("http://anekdotme.ru/random")
    soup = bs4.BeautifulSoup(req_anek.text, "html.parser")
    result_find = soup.select('.anekdot_text')
    for result in result_find:
        array_anekdots.append(result.getText().strip())
    return array_anekdots[0]
