def read_file():
    with open('Q:\\tg_bot\\money.txt', 'r', encoding='utf-8') as file:
        token = file.read()
    return token