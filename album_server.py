import os
import json
import album
from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request


RESOURCES_PATH = "users/"


class InvalidDataValue(Exception):
    """
    Используется для проверки остальных данных. В данном случае будем проверять, что значение не пустое.
    """
    pass


def validate(data):
    """
    Проверка сохраняемых данных на корректность.
    У года проверяем, что длина строки = 4 и все символы - цифры.
    У остальных параметров, просто наличие данных
    """
    print(data)
    result = True
    for p in data:
        print(p, data[p])
        if data[p] is None:
            raise InvalidDataValue("Параметр {} отсутствует!".format(p))
        elif len(data[p]) == 0:
            raise InvalidDataValue("Длина парметра {} равна нулю!".format(p))
        elif p == "year" and (len(data[p]) != 4 or not data[p].isdigit()):
            raise InvalidDataValue("Некорректное значение параметра {}".format(p))
    return result


def save_album(new_data):
    album.savetodb(new_data)


@route("/new_album", method="POST")
def new_album():
    album_data = {
        "artist": request.forms.get("artist"),
        "year": request.forms.get("year"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album")
    }
    if validate(album_data):
        # Поиск по паре Артист+Альбом
        albums_list = album.find(album_data["artist"], album_data["album"])
        # Проверяем длину списка
        p = len(albums_list)
        # Если длина списка = 0, то записываем в БД
        if p == 0:
            save_album(album_data)
            print("User saved to DB")
            return "Данные успешно сохранены"
        else:
            return HTTPError(409, "Альбом уже есть в БД!")


@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    p = len(albums_list)
    print(p)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        result = "Количество альбомов: {}<br>".format(str(p))
        album_names = [album.album for album in albums_list]
        result += "Список альбомов {}:<br>".format(artist)
        result += "<br>".join(album_names)
    return result


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)