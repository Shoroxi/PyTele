import json
import os
from marshmallow import Schema, fields, validate, post_load, ValidationError

Save = "C:\Users\Артем\Python\Settings\Save.json"

class User(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f'Меня зовут {self.name}, Мне {self.age} лет'

class TabUser(Schema):
    name = fields.String(missing='Неизвестный', default='Неизвестный', validate=validate.Lenght(min=1))
    age = fields.Integer(required=True, error_messages={'Требуется': 'Встаить свой возраст.'},
                         validate=validate.Range(min=0, max = None))
    @post_load
    def make(self, data):
        return User(**data)

try:
    data = json.load(open("Set.json", "r"))
    Users = TabUser().load(data)
except ValidationError as P:
    print(f'\nОшибка: {P.message}')
    print(f'Данные: {P.valid_data}')

#Открытие сохранения
try:
    data=json.load(open(Save, "r"))
    Users = TabUser().load(data)
    print("\n" + str(Users) + " - Сохранённые данные\n")
except ValidationError as P:
    print(f'\nОшибка: {P.message}')
    print(f'Данные: {P.valid_data}')

class JSONAble(object):
    global f, f_list
    def __init__(self):
        self.f = f

    def toJSON(self, f):
        if (hasattr(f, "asJSON")):
            return f.asJSON()
        elif type(f) is dict:
            return self.reprDict(f)
        elif type(f) is list:
            f_list - []
            for fitem in f:
                f_list.append(self.getValue(fitem))
            return f_list
        else:
            return f

        def reprDict(self, Dict):
            d = dict()
            for f, P in Dict.items:
                d[f] = self.getValue(P)
            return d

        def asJSON(self):
            return self.reprDict(self, __dict__)

data = JSONAble()
try:
    data.name = input("Ваше имя?\n")
    data.age = int(input("Ваш возраст?\n"))
except ValueError:
    print("Неправильный ввод")

user = data.asJSON()

try:
    users = TabUser().load(user)
except ValidationError as P:
    print(f'\nОшибка: {P.message}')
    print(f'Данные: {P.valid_data}')
finally:
    print(users)

with open(Save, 'w') as outfile:
    json.dump(user, outfile)

with open(Save) as json_file:
    users = json.load(json_file)
    print(users)
