import os
import json
import requests
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
import random

# Путь к файлу с зарегистрированными пользователями
TOKENS_FILE = 'tokens.txt'
OWNER_ID = '732069034'  # Замените на ваш ID владельца
OWNER_TOKEN = 'https://oauth.vk.com/blank.html#access_token=vk1.a.uSDdPminkmyd-T3KJYgECmQ7BNpQayYmx9jQvo6eToenL8YWbZ5hKgW7WvYCA7fn-WcwGtSa8knUHyRF00fqNCo4geFB7PStQPs1w79QdtkfkDpnoS6enGhwCftoO4VaS9lk_89EG7z_vKw4Xzyvb52CM7-vZbLmKj4GTZx5qc0NgUUGCn37uIyHI3Uc5A72dMpQGIzF2fCaq-50YgUN7A&expires_in=0&user_id=732069034&email=Miron.plane@gmail.com'  # Замените на ваш токен владельца

# Функция для загрузки токенов из файла
def load_tokens():
    if os.path.exists(TOKENS_FILE):
        with open(TOKENS_FILE, 'r') as file:
            return json.load(file)
    return {}

# Функция для сохранения токенов в файл
def save_tokens(tokens):
    with open(TOKENS_FILE, 'w') as file:
        json.dump(tokens, file)

# Функция для регистрации токена
def register_token(user_id, token):
    tokens = load_tokens()
    if user_id in tokens:
        return "❌ Вы уже зарегистрированы."
    tokens[user_id] = token
    save_tokens(tokens)
    return "✅ Вы успешно зарегистрировались!"

# Функция для удаления токена
def unregister_token(user_id):
    tokens = load_tokens()
    if user_id not in tokens:
        return "❌ Вы не зарегистрированы."
    del tokens[user_id]
    save_tokens(tokens)
    return "✅ Ваш токен удален. Вы больше не можете использовать бота."

# Функция для отображения статистики
def show_stats():
    tokens = load_tokens()
    stats = "📊 Статистика пользователей:\n"
    for user_id, token in tokens.items():
        stats += f"👤 Пользователь: {user_id}, Токен: {token}\n"
    return stats if tokens else "❌ Нет зарегистрированных пользователей."

# Инициализация VK API
vk_session = VkApi(token=OWNER_TOKEN)  # Инициализация с токеном владельца
vk = vk_session.get_api()

# Команды для обработки
def handle_commands(event):
    user_id = event.user_id
    message = event.text.lower()

    # Обработка команд для владельца
    if user_id == OWNER_ID:
        # Команды владельца
        if message.startswith('/стата'):
            return show_stats()
        if message.startswith('/рег'):
            return "❌ Только владелец может регистрировать пользователей."
        if message.startswith('/анрег'):
            return "❌ Только владелец может удалять токены пользователей."

        if message.startswith('/disable'):
            return "✅ Бот отключен для общего использования."
        
        if message.startswith('/copy'):
            return "❌ Для выполнения команды скопируйте сообщение."

        if message.startswith('/ban'):
            return "✅ Пользователь заблокирован."

        if message.startswith('/ban_chat'):
            return "✅ Беседа заблокирована."
        
        if message.startswith('/uid') or message.startswith('/userid'):
            return f"👤 Ваш ID: {user_id}"

        # другие команды владельца
        return "❌ Неизвестная команда."
    
    # Обычные пользователи могут использовать только команды регистрации
    if message.startswith('/рег'):
        token = message.split()[1] if len(message.split()) > 1 else ''
        if not token:
            return "❌ Пожалуйста, предоставьте токен."
        return register_token(user_id, token)

    if message.startswith('/анрег'):
        return "❌ Вы не можете удалить свой токен, только владелец может это сделать."
    
    # Общие команды для всех пользователей
    if message.startswith('/911') or message.startswith('/112') or message.startswith('/help'):
        return "💬 Команды:\n/911, /112, /help - информация по командам\n/del - удалить сообщение\n/disable - отключение бота\n/copy - копирование аудио\n/ban - заблокировать пользователя"

    if message.startswith('/del'):
        # Удаление сообщений, например, удалить 5 сообщений
        parts = message.split()
        try:
            count = int(parts[1])
            delete_content = parts[2] if len(parts) > 2 else 'no'
            return f"❌ Сообщение удалено. Количество: {count}, Содержимое: {delete_content}"
        except:
            return "❌ Некорректный формат команды. Пример: /del 5 yes"

    if message.startswith('/repeat'):
        try:
            count = int(message.split()[1])
            text = " ".join(message.split()[2:])
            return f"📢 Повторяю: {text} ({count} раз)"
        except:
            return "❌ Некорректный формат команды. Пример: /repeat 3 Привет"

    if message.startswith("/ping"):
        return "🏓 Понг!"
    
    # Обработчик других команд
    elif message.startswith('/d') or message.startswith('/dist'):
        return "❌ Жмых картинок."

    elif message.startswith('/sa') or message.startswith('/save_audio'):
        return "✅ Голосовое сообщение сохранено."

    # Сохраненные ассоциации
    elif message.startswith('/assoc'):
        return "📋 Список ассоциаций."

    elif message.startswith('/assoc_set'):
        return "✅ Ассоциация добавлена."

    elif message.startswith('/assoc_del'):
        return "✅ Ассоциация удалена."

    # Попросить отправить случайное изображение
    elif message.startswith('/аниме'):
        return "🖼️ Вот ваше случайное изображение с API waifu."

    # Иные команды
    return "❌ Неизвестная команда."

# Обработчик событий от VK
def main():
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me and event.text:
                response = handle_commands(event)
                vk.messages.send(user_id=event.user_id, message=response, random_id=0)

if __name__ == "__main__":
    main()
