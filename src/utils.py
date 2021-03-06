import os
import sys
from PIL import Image
import string
import base64
import json
import unicodedata
from colorama import Fore
from line_filters import lineFilter


SIZE = 5


def save_candidate_name(path, image, icon_name, count):
    newImg = lineFilter(image)
    newImg.save(path + handle_name(icon_name) + '_' + str(count) + '.png')


def list_individual_images(path):
    for f in os.listdir(path):
        if f in [".DS_Store", ".gitkeep"]:
            continue
        filename = path + f
        image = Image.open(filename)
        yield f, image


def break_captcha(path, icon_name, image):
    total_width = image.size[0]
    total_height = image.size[1]
    width_icon = total_width / SIZE

    for i, col in enumerate(range(0, total_width, int(width_icon))):
        coords = (col, 0, col+width_icon, total_height)
        image_icon = image.crop(coords)
        save_candidate_name(path, image_icon, icon_name, i)
        yield icon_name, image_icon


chars = string.ascii_letters + ' ' + '_' + string.digits

def handle_name(data):
    return ''.join(x for x in unicodedata.normalize('NFKD', data) if x in chars).lower()


def save_image(folder, icon, data_b64):
    filename = f"{folder}{handle_name(icon)}.png"
    with open(filename, "wb") as fh:
        fh.write(base64.urlsafe_b64decode(data_b64))


from http.cookies import SimpleCookie

def cookie_string_to_mapping(text):
    cookie = SimpleCookie()
    cookie.load(text)
    cookies = {}
    for key, morsel in cookie.items():
        cookies[key] = morsel.value
    return cookies


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def read_configuration_file():
    with open(resource_path('config.json')) as file:
        arguments = json.load(file)

    credentials = arguments['credentials']
    part = arguments['participant']

    if part not in [1,2,3]:
        raise Exception("Você precisa escolher entre 1, 2 e 3 no config.json para votar.")

    try:
        username = credentials[0]['username']
        password = credentials[0]['password']
    except IndexError as e:
        raise Exception(Fore.RED + "Você precisa preencher pelo menos um nome de usuário e senha.")
    return arguments
