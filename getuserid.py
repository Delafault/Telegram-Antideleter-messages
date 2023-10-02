#Скрипт для получения userId пользователей (сразу записывает все найденные userId в config.ini)

from pyrogram import Client
import os
import configparser

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    print("1. Настройка api_id и api_hash")
    print("2. Настройка номера телефона")
    print("3. Запустить скрипт")

def change_api_id():
    global api_id
    global api_hash
    new_api_id = input("Введите api_id: ")
    api_id = int(new_api_id)
    new_api_hash = input("Введите api_hash: ")
    api_hash = new_api_hash
    save_config()

def change_phone_number():
    global phone_number
    phone_number = input("Введите номер телефона: ")
    save_config()

def save_config():
    config = configparser.ConfigParser()
    config['User'] = {
        'api_id': str(api_id),
        'api_hash': api_hash,
        'phone_number': phone_number
    }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

config = configparser.ConfigParser()

if os.path.exists('config.ini'):
    config.read('config.ini')
    api_id = config['User'].get('api_id', '')
    api_hash = config['User'].get('api_hash', '')
    phone_number = config['User'].get('phone_number', '')
else:
    api_id = ''
    api_hash = ''
    phone_number = ''

clear_console()
while True:
    display_menu()
    choice = input("Выберите опцию (1, 2, 3): ")
    
    if choice == '1':
        change_api_id()
        clear_console()
    elif choice == '2':
        change_phone_number()
        clear_console()
    elif choice == '3':
        if not api_id or not api_hash or not phone_number:
            clear_console()
            print("\nПожалуйста, заполните все поля (api_id, api_hash и номер телефона) перед запуском скрипта.\n")
        else:
            break
    else:
        input("Неверный выбор. Нажмите Enter для продолжения...")

app = Client('SESSION_FOR_CONTROL_DELETEMSG2', api_id, api_hash, device_model="Pixel 3 XL", system_version="Android 10.0", phone_number = phone_number)




def update_ignore_users():
    global user_ids
    with open('config.ini', 'r') as configfile:
        config.read_file(configfile)
        config.set('User', 'ignore_users', ', '.join(user_ids))
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def save_user_ids():
    global user_ids
    usernames = input("Введите имена пользователей (разделите пробелами): ").split()

    user_ids = []

    for username in usernames:
        try:
            user = app.get_users(username)
            user_ids.append(str(user.id))
        except Exception as e:
            print(f"Не удалось получить информацию о пользователе {username}: {e}")

    update_ignore_users()
    print("UserId сохранены в строке 'ignore_users' в файле config.ini")




with app:
    save_user_ids()