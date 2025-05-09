def read_file():
    with open('Q:\\my_pet_projact\\money_test.txt', 'r', encoding='utf-8') as file:
        token = file.read()
    return token