import telebot
from telebot import types

TOKEN = '8093972019:AAGvqREA-TupQWVT1HGJ0i2SAQeKoTznKuA'
ADMIN_ID = 7532239854
bot = telebot.TeleBot(TOKEN)

prices = {
    'Standoff 2': {
        '100 голды': (19000, '🔥 Популярно'),
        '500 голды': (79500, '💰 Выгодно'),
        '1000 голды': (141500, '⭐ Топ продаж'),
        '3000 голды': (318000, '🚀 Максимум'),
    },
    'PUBG Mobile': {
        '60 UC': (11500, '🔸 Маленький пакет'),
        '325 UC': (58000, '🔹 Мини'),
        '660 UC': (130800, '💥 Популярно'),
        '1800 UC': (291800, '🔥 Выгодно'),
        '3850 UC': (583600, '🚀 Максимум'),
        '8100 UC': (1167300, '💎 Премиум'),
        '16200 UC': (2333000, '💰 Большой пакет'),
        '24300 UC': (3496000, '⚡ Очень большой'),
        '32400 UC': (4667000, '🔥 Супер пакет'),
        '40500 UC': (5834000, '💎 Элитный'),
        '81000 UC': (11668000, '🚀 Мега пакет'),
    },
    'Brawl Stars': {
        '30 гемов': (29700, '🔹 Стартовый'),
        '80 гемов': (71200, '🔸 Популярный'),
        '170 гемов': (142500, '🔥 Топ выбор'),
        '360 гемов': (285400, '💰 Выгодно'),
        '950 гемов': (713400, '💎 Премиум'),
    }
}

promocodes = {
    'WELCOME100': 100000,
    'DISCOUNT50': 50000,
}

user_balances = {}
user_states = {}

def main_menu(chat_id):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add('💰 Купить', '📊 Баланс', '👤 Профиль', '💵 Пополнить баланс',
           '🎁 Промокод', '🛠 Поддержка', '🌟 Отзывы')
    bot.send_message(chat_id, "📋 Главное меню. Выберите действие:", reply_markup=kb)

@bot.message_handler(commands=['start'])
def start(message):
    user_balances.setdefault(message.chat.id, 0)
    user_states.pop(message.chat.id, None)
    main_menu(message.chat.id)

@bot.message_handler(commands=['addbalance'])
def add_balance(message):
    if message.from_user.id != ADMIN_ID:
        return bot.reply_to(message, "⛔ У вас нет прав.")
    try:
        _, user_id, amount = message.text.split()
        user_id, amount = int(user_id), int(amount)
        user_balances[user_id] = user_balances.get(user_id, 0) + amount
        bot.send_message(user_id, f"✅ Баланс пополнен на {amount:,} сум!")
        bot.reply_to(message, f"Успешно пополнено пользователю {user_id}.")
    except:
        bot.reply_to(message, "❌ Используйте: /addbalance <id> <сумма>")

@bot.message_handler(commands=['chat'])
def admin_chat(message):
    if message.from_user.id != ADMIN_ID:
        return bot.reply_to(message, "⛔ У вас нет прав.")
    try:
        parts = message.text.split(maxsplit=2)
        user_id, msg = int(parts[1]), parts[2]
        bot.send_message(user_id, f"📨 Сообщение от поддержки:\n\n{msg}")
        bot.reply_to(message, "✅ Сообщение отправлено.")
    except:
        bot.reply_to(message, "❌ Использование: /chat <id> <сообщение>")

@bot.message_handler(func=lambda m: m.text == '📊 Баланс')
def balance(message):
    bal = user_balances.get(message.chat.id, 0)
    bot.send_message(message.chat.id, f"💰 Ваш баланс: {bal:,} сум")

@bot.message_handler(func=lambda m: m.text == '👤 Профиль')
def profile(message):
    bot.send_message(message.chat.id, f"🆔 Ваш Telegram ID:\n{message.chat.id}")

@bot.message_handler(func=lambda m: m.text == '🎁 Промокод')
def promocode(message):
    user_states[message.chat.id] = {'action': 'promocode'}
    bot.send_message(message.chat.id, "🔑 Введите промокод:")

@bot.message_handler(func=lambda m: m.text == '💵 Пополнить баланс')
def popolnit(message):
    user_states[message.chat.id] = {'action': 'waiting_screenshot'}
    bot.send_message(message.chat.id, "💳 Переведите деньги на карту:\n4916 9903 1018 5019\n\nПосле оплаты отправьте скриншот сюда.")

@bot.message_handler(func=lambda m: m.text == '🛠 Поддержка')
def support(message):
    bot.send_message(message.chat.id, "📩 Связь с поддержкой: @equikk1")

@bot.message_handler(func=lambda m: m.text == '🌟 Отзывы')
def reviews(message):
    bot.send_message(message.chat.id, "🔗 Отзывы: https://t.me/Ggbalancee")

@bot.message_handler(func=lambda m: m.text == '💰 Купить')
def buy(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add('🎮 Standoff 2', '🔫 PUBG Mobile', '⭐ Brawl Stars', '🔙 Назад')
    bot.send_message(message.chat.id, "Выберите игру:", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text in ['🎮 Standoff 2', '🔫 PUBG Mobile', '⭐ Brawl Stars'])
def prices_list(message):
    game = message.text[2:].strip()  # убираем эмоджи + пробел
    user_states[message.chat.id] = {'action': 'choose_item', 'game': game}
    text = f"💵 Цены для {game}:\n\n"
    items = []
    for item, (price, desc) in prices[game].items():
        text += f"{item} — {price:,} сум — {desc}\n"
        items.append(item)
    user_states[message.chat.id]['items'] = items
    bot.send_message(message.chat.id, text)
    bot.send_message(message.chat.id, "✍️ Напишите точное название пакета:")

@bot.message_handler(func=lambda m: m.text == '🔙 Назад')
def back(message):
    user_states.pop(message.chat.id, None)
    main_menu(message.chat.id)

@bot.message_handler(func=lambda m: True, content_types=['text'])
def handle_text(message):
    uid = message.chat.id
    state = user_states.get(uid)
    if not state:
        return main_menu(uid)

    action = state.get('action')
    if action == 'promocode':
        code = message.text.strip().upper()
        if code in promocodes:
            user_balances[uid] = user_balances.get(uid, 0) + promocodes[code]
            bot.send_message(uid, f"🎉 Промокод активирован! Баланс пополнен на {promocodes[code]:,} сум.")
        else:
            bot.send_message(uid, "❌ Неверный промокод.")
        user_states.pop(uid)
        main_menu(uid)

    elif action == 'choose_item':
        item = message.text.strip()
        if item in state['items']:
            price = prices[state['game']][item][0]
            if user_balances.get(uid, 0) < price:
                bot.send_message(uid, f"⛔ Недостаточно средств! Цена: {price:,} сум")
                user_states.pop(uid)
                main_menu(uid)
                return
            user_states[uid] = {'action': 'waiting_game_id', 'game': state['game'], 'item': item, 'price': price}
            bot.send_message(uid, "🔑 Введите ваш игровой TAG/ID:")
        else:
            bot.send_message(uid, "❗ Введите точно как написано.")

    elif action == 'waiting_game_id':
        tag = message.text.strip()
        price, game, item = state['price'], state['game'], state['item']
        user_balances[uid] -= price
        bot.send_message(uid, "✅ Заказ отправлен в обработку. Ожидайте подтверждения.")
        bot.send_message(ADMIN_ID, f"""📦 Новый заказ:
Пользователь: @{message.from_user.username or 'Без ника'} ({uid})
Игра: {game}
Пакет: {item}
TAG/ID: {tag}
Сумма: {price:,} сум
Баланс после: {user_balances[uid]:,} сум

Для подтверждения: /chat {uid} Заказ выполнен ✅""")
        user_states.pop(uid)
        main_menu(uid)

    else:
        main_menu(uid)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    uid = message.chat.id
    state = user_states.get(uid)
    if state and state.get('action') == 'waiting_screenshot':
        bot.forward_message(ADMIN_ID, uid, message.message_id)
        bot.send_message(uid, "📤 Скриншот отправлен в поддержку.\nТеперь нажмите «👤 Профиль» и отправьте ваш ID.")
        user_states.pop(uid)
    else:
        bot.send_message(uid, "⚠️ Если это скриншот оплаты, сначала выберите 'Пополнить баланс'.")

bot.polling(none_stop=True)
