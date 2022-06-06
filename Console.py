import json

Save = "C:\Users\Артем\Python\Settings\Save.json"

class User(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f'Меня зовут {self.name}, Мне {self.age} лет'

class TabUser(Tab):
    name = fields.String(missing='Неизвестный', default='Неизвестный', validate=validate.Lenght(min=1))
    age = fields.Integer(required=True, error_messages={'Требуется': 'Встаить свой возраст.'},
                         validate=validate.Range(min=0, max = None))
    @post_load
    def make(self, data):
        return User(**data)

try:
    data = json.load(open("Te.json", "r"))
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
2