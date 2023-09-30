from pyrogram import Client, filters
from datetime import datetime
import logging
from colorama import Fore, Style, init
import os
import configparser

init()

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
while not api_id or not api_hash or not phone_number:
    display_menu()
    choice = input("Выберите опцию (1, 2 или 3): ")
    
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

received_messages = {}

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_message_type(message):
    if message.photo:
        return "фотография"
    elif message.sticker:
        return "стикер"
    elif message.animation:
        return "гифка"
    elif message.video:
        return "видео"
    elif message.document:
        return "документ"
    elif message.audio:
        return "аудио"
    elif message.voice:
        return "голосовое сообщение"
    elif message.forward_from or message.forward_from_chat:
        return "пересланное сообщение"
    else:
        return "текст"

@app.on_message(filters.private)
async def handle_private_message(client, message):
    message_id = message.id
    message_content = message.text or message.caption
    sender_id = message.from_user.id
    sender_username = message.from_user.username
    message_type = get_message_type(message)
    
    if sender_id != app.me.id:
        log_message = f"[Новое сообщение в ЛС] ID: {message_id} | Отправитель: @{sender_username} ({sender_id}) | Тип сообщения: {message_type}"
        print(Fore.GREEN + log_message + Style.RESET_ALL)
        #logging.info(log_message)
    
    received_messages[message_id] = {
        'content': message_content,
        'sender_id': sender_id,
        'sender_username': sender_username,
        'message_type': message_type
    }

@app.on_deleted_messages()
async def handle_deleted_message(client, messages):
    for message in messages:
        message_id = message.id
        delete_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if message_id in received_messages:
            content = received_messages[message_id]['content']
            sender_id = received_messages[message_id]['sender_id']
            sender_username = received_messages[message_id]['sender_username']
            message_type = received_messages[message_id]['message_type']
            
            if sender_id == app.me.id:
                textmsg = f"Ваше сообщение было удалено: {content}\nВремя удаления: {delete_time}\nТип сообщения: {message_type}"
                await app.send_message("me", textmsg)
                log_message = f"[Ваше сообщение было удалено] Время удаления: {delete_time} | Тип сообщения: {message_type}"
                print(Fore.RED + log_message + Style.RESET_ALL)
                #logging.info(log_message)
            else:
                textmsg = f"Удалено сообщение в ЛС:\nID: {message_id}\nСодержимое: {content}\nОтправитель: @{sender_username} ({sender_id})\nВремя удаления: {delete_time}\nТип сообщения: {message_type}"
                await app.send_message("me", textmsg)
                log_message = f"[Удалено сообщение в ЛС] ID: {message_id} | Отправитель: @{sender_username} ({sender_id}) | Время удаления: {delete_time} | Тип сообщения: {message_type}"
                print(Fore.RED + log_message + Style.RESET_ALL)
                #logging.info(log_message)
        else:
            log_message = f"[Удалено сообщение] ID: {message_id} | Информация о сообщении отсутствует | Время удаления: {delete_time}"
            print(Fore.RED + log_message + Style.RESET_ALL)
            # logging.info(log_message)
            pass

clear_console()
print("""
▄▀█ █▄░█ ▀█▀ █ █▀▄ █▀▀ █░░ █▀▀ ▀█▀ █▀▀ █▀█ █▀▄▀█ █▀ █▀▀|ᵇʸ ᵈᵉˡᵃᶠᵃᵘˡᵗ
█▀█ █░▀█ ░█░ █ █▄▀ ██▄ █▄▄ ██▄ ░█░ ██▄ █▀▄ █░▀░█ ▄█ █▄█
      FOR TELEGRAM (version 0.1)\n\n""")

app.run()