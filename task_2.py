from hashlib import pbkdf2_hmac
from binascii import hexlify
from sys import argv

script_name, path_to_input, path_to_dir = argv


def hash_func(f_file_name):
    """
    Функция принимает даные из файла, хеширует и солит
    заданное количество раз, преобразовывает в 16-тиричную
    строку и переводит в строку, которую можно сравнить
    с хешем из входного файла.
    """
    try:
        with open(f'{path_to_dir}/{f_file_name}', "r") as file:
            content = ''.join(file.readlines())

        obj = pbkdf2_hmac(hash_name=encoding_algorithm,
                          password=content.encode(),
                          salt=f_file_name.encode(),
                          iterations=1000)
        res = hexlify(obj)
        return res.decode()
    except FileNotFoundError:
        return "NOT FOUND"


with open(path_to_input, "r") as data_file:
    data_str = data_file.readlines()
    str_el = [el.split() for el in data_str]

    for i in str_el:
        try:
            file_name = i[0]
            encoding_algorithm = i[1]
            hash_content = i[2]
            if hash_func(file_name) == "NOT FOUND":
                print(f'{file_name} NOT FOUND')
            elif hash_func(file_name) == hash_content:
                print(f'{file_name} OK')
            elif hash_func(file_name) != hash_content:
                print(f'{file_name} FAIL')
        except IndexError:
            print(f'{file_name} FAIL')
