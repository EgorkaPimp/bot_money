def read_file():
    with open('/home/egor/token/money.txt', 'r', encoding='utf-8') as file:
        token = file.read()
    return token