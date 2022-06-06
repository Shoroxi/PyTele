import os
import json

class object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=False, indent=4)

Str = object()
Str.name = input("Введите имя\n")

file = input("Путь к файлу\n")
if os.path.exists(file):
    Str.f = "Y"
else:
    Str.f = "N"

Del = input("Удалить файл?")
if Del == "да":
    os.remove(file)
    Str.dl = "Y"
elif Del == "нет":
    Str.dl = "N"