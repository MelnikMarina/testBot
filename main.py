import sqlite3
import telebot
from telebot import types
from aiogram.types import InlineKeyboardButton, KeyboardButton, WebAppInfo, ReplyKeyboardMarkup
from datetime import datetime

id_seller = [6131680389,]
TOKEN = '6066868239:AAF6j0ELFVyuWa1khfDMCDLxiBghUMMxGt4' #@selmot_bot
bot = telebot.TeleBot(TOKEN)

global db
global sql

db = sqlite3.connect('TuttyFrutty.db', check_same_thread=False)
sql = db.cursor()

sql.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "name TEXT, price BIGINT, count BIGINT, discount BIGINT DEFAULT 0,"
            "final_price BIGINT GENERATED ALWAYS AS (Price * (100 - Discount) / 100) STORED)") #Таблица с продуктами

sql.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "user_name TEXT, user_id BIGINT, balance BIGINT)") #Таблица с пользователями

sql.execute("CREATE TABLE IF NOT EXISTS status (id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "user_id BIGINT, order_id INT, order_status INT)")
            #0 - заказ оформлен, #1 - заказ подтвержден, #2 заказ отправлен. Все регулирует продавец

sql.execute("CREATE TABLE IF NOT EXISTS cart (id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "number_order, user_id BIGINT, id_product BIGINT, count BIGINT)") #Таблица с корзинами

@bot.message_handler(commands = ['start']) #Обработка команды /start
def register(message):
    add_default_product_list()
    username = message.from_user.username; user_id = message.from_user.id; balance = 0
    sql.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    if sql.fetchone() is None:
        sql.execute(
            f"INSERT INTO users (user_name, user_id, balance) VALUES ('{message.from_user.username}', '{message.from_user.id}', {0})")
            #Вставить значения в таблицу. (Название ячеек) (Сами переменные)
        db.commit() #Сохранение изменения в БД
        bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}! Добро пожаловать в магазин.')
        buttons(message)
    else:
        bot.send_message(message.chat.id, f'C возвращением, {message.from_user.first_name}! Добро пожаловать в магазин.')
        buttons(message)


def add_default_product_list():
    sql.execute("delete from products")
    sql.execute("delete from sqlite_sequence where name='products'")
    db.commit()
    sql.execute(
        f"INSERT INTO products (name, price, count, discount)"
        f"VALUES"
        f"('Red Printed T-shirt', {3000}, {5}, {0}),"
        f"('Black Sneakers', {5000}, {5}, {0}),"
        f"('Gym trousers', {2000}, {5}, {0}),"
        f"('Navy Puma Polo', {4000}, {5}, {0}),"
        f"('Air Jordan I', {10000}, {5}, {0}),"
        f"('Puma T-shirt', {5000}, {5}, {0}),"
        f"('3 Pair Socks Set', {1000}, {5}, {0}),"
        f"('Black Fossil Watch', {12000}, {5}, {0}),"
        f"('Leather Band Cassio Watch', {15000}, {5}, {0})"
    )
    db.commit()


def otzovikto(message): #Добавление функции отзывов
    text_for_otzyv = message.text
    if message.text:
        markup_inline = types.InlineKeyboardMarkup(row_width = 2)
        item_accept = types.InlineKeyboardButton(text = 'Отправить продавцу', callback_data = 'publish_otz')
        item_decline = types.InlineKeyboardButton(text = 'Отклонить', callback_data = 'decline_otz')
        markup_inline.add(item_accept, item_decline)
        bot.send_message(message.chat.id, f"{text_for_otzyv}", reply_markup = markup_inline)


@bot.message_handler(commands = ['otzyv']) #Обработка команды /otzyv
def otzovik(message):
    msg = bot.send_message(message.chat.id, '📝 Напишите свой отзыв: ')
    bot.register_next_step_handler(msg, otzovikto)

@bot.message_handler(commands = ['menu']) #Обработка команды /menu
def buttons(message):
    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True) #Создание клавиатуры
    item_catalog = types.KeyboardButton(text = '📓 Каталог товаров')
    item_profile = types.KeyboardButton(text = '👨🏻‍💻 Мой профиль')
    markup_reply.add(item_catalog, item_profile) #Добавление кнопок в клавиатуру
    bot.send_message(message.chat.id, 'Выберите опцию меню:',
        reply_markup = markup_reply
    )

def webAppKeyboard(): #создание клавиатуры с webapp кнопкой
   keyboard = types.ReplyKeyboardMarkup(row_width=1) #создаем клавиатуру
   webAppTest = types.WebAppInfo("https://melnikmarina.github.io/TwDB/") #создаем webappinfo - формат хранения url
   one_butt = types.KeyboardButton(text="Selmot_shop", web_app=webAppTest) #создаем кнопку типа webapp
   keyboard.add(one_butt) #добавляем кнопки в клавиатуру

   return keyboard #возвращаем клавиатуру


@bot.message_handler(content_types = ['text']) #Обработчик текста
def get_text(message):
    if message.text == '📓 Каталог товаров':
        bot.send_message(message.chat.id, 'Вы открыли каталог',reply_markup=webAppKeyboard())

    elif message.text == '🔎 Поиск товара':
        bot.send_message(message.chat.id, f'Функция в процессе разработки.') # Марина

    elif message.text == '👨🏻‍💻 Мой профиль':
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        сheck_balance = types.KeyboardButton(text = '💵 Проверить баланс')
        check_status = types.KeyboardButton(text='💡 Проверить статус заказа')
        go_back = types.KeyboardButton(text='❌ Отменить заказ')
        delete = types.KeyboardButton(text='⏪ Вернуться в меню')
        seller_menu = types.KeyboardButton(text='💼 Зайти в меню продавца')
        markup_reply.add(сheck_balance, check_status, go_back, delete,seller_menu)
        bot.send_message(message.chat.id, 'Личный кабинет:',
                         reply_markup=markup_reply
                         )

    elif message.text == '💵 Проверить баланс':
        user_id = message.from_user.id
        sql.execute(f"SELECT balance FROM users WHERE user_id = {user_id}")
        result = sql.fetchone()
        if result: #Проверяем есть ли запись в БД
            balance = result[0]
            bot.send_message(message.chat.id, f'Ваш баланс: {balance} 💳')
        else: #Если её нет, тогда выполняем другое условие
            bot.send_message(message.chat.id, f'Пользователь #{message.from_user.id} не найден')

    elif message.text == '💡 Проверить статус заказа':
        user_id = message.from_user.id
        now = datetime.now()
        datetime_str = now.strftime("%d.%m.%Y %H:%M")
        sql.execute(f"SELECT id, user_id, order_status FROM status WHERE user_id = {user_id}") #Выбираем, что достаем. Выбираем откуда. Выбираем фильтр для отбора
        results = sql.fetchall() #fetchall() записываешь все данные, которые собрал по запросу в БД
        order_list = ""
        if results:
            for result in results:
                id, user_id, order_status = result
                if order_status == 0:
                    order_list += f'\nЗаказ #{id} успешно оформлен 📝 Ожидайте подтверждения! \n'
                if order_status == 1:
                    order_list += f'\nЗаказ #{id} был подтвержден продавцом ✅ Ожидайте отправления! \n'
                if order_status == 2:
                    order_list += f'\nЗаказ #{id} был отправлен продавцом 📦 При получении вы можете оставить отзыв - /otzyv\n'
            bot.send_message(message.chat.id, f'{message.from_user.first_name}, список ваших актуальных заказов на {datetime_str}: \n'
                                              f'\n{order_list}')
        else:
            bot.send_message(message.chat.id, f'{message.from_user.first_name}, у вас на данный момент нет активных заказов 😦')

    elif message.text == '❌ Отменить заказ':
        user_id = message.from_user.id
        sql.execute(f"SELECT id, user_id, order_status FROM status WHERE user_id = {user_id}")
        result = sql.fetchone()
        if result is not None:
            id, user_id, order_status = result
            markup = types.InlineKeyboardMarkup() #Кнопки в самом сообщении
            confirm = types.InlineKeyboardButton(text="Да ✔", callback_data=f"confirm_delete") #callback_data для работы в callback_handler
            cancel = types.InlineKeyboardButton(text="Нет ✖", callback_data=f"cancel_delete")
            markup.add(confirm, cancel)
            bot.send_message(message.chat.id,
                             f'Вы действительно хотите удалить свои заказы?',
                             reply_markup=markup)
            return id
        else:
            bot.send_message(message.chat.id,
                             f'{message.from_user.first_name}, у вас на данный момент нет активных заказов 😦')

    elif message.text == '⏪ Вернуться в меню':
        markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Создание клавиатуры
        item_catalog = types.KeyboardButton(text='📓 Каталог товаров')
        item_profile = types.KeyboardButton(text='👨🏻‍💻 Мой профиль')
        markup_menu.add(item_catalog, item_profile)  # Добавление кнопок в клавиатуру
        bot.send_message(message.chat.id, 'Возвращаемся в главное меню:',
                         reply_markup = markup_menu)

    elif message.text == '💼 Зайти в меню продавца' or '/seller': #Меню продавца-администратора
        user_id = message.from_user.id
        if user_id in id_seller:
            bot.send_message(message.chat.id, f'Функция в процессе разработки.') #Богдан
        else:
            bot.send_message(message.chat.id, f'В доступе отказано.')


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "confirm_delete": #Подтверждение удаление заказа
        user_id = call.message.chat.id
        sql.execute(f"DELETE FROM status WHERE user_id = {user_id}")
        db.commit()
        bot.send_message(call.message.chat.id, f'Ваш заказ успешно удален!')

    elif call.data == "cancel_delete": #Отмена удаления заказа
        bot.send_message(call.message.chat.id, f'Вы отменили удаление заказа.')

    elif call.data == "confirm_cart":
        '''Подтверждение корзины покупателем. Дальше идёт проверка хватит ли у него средств для осуществления покупки.
        После чего, если средств достаточно, бот спрашивает адрес и происходит подтверждение заказа. В этот момент
        удаляется корзина и забираются продукты из "products" и оформляется новый заказ в "status". 
        Одновременно продавцы получают оповещение что пользователь совершил покупку и содержание его заказа.
        В случае, если денег нет, тогда покупатель не сможет оформить покупку и его корзина обнуляется.'''
        user_id = call.message.chat.id
        sql.execute(f"SELECT balance FROM users WHERE user_id = {user_id}")
        balance = sql.fetchone()[0]
        final_sum = 0

        def change_balance(): #Изменение баланса пользователя после совершения покупки
            sql.execute(f"UPDATE users SET balance = balance - {final_sum} where user_id = {user_id}")
            db.commit()

        sql.execute(f"SELECT id_product, count FROM cart where user_id = {user_id}") #Проверка стоимости всей корзины
        rows = sql.fetchall()
        for row in rows:
            id_product, count = row
            sql.execute(f"SELECT final_price FROM products WHERE id = {id_product}")
            price = sql.fetchone()[0]
            final_sum += price*count

        def get_cart(message):  # Оформление карзины с получением адреса от пользователя
            address = message.text
            user_id = message.chat.id;
            user_name = message.chat.username
            sql.execute(f"SELECT number_order, id_product, count FROM cart where user_id = {user_id}")
            order_list = ""
            rows = sql.fetchall()
            for row in rows:
                number_order, id_product, count = row
                sql.execute(f"UPDATE products SET count = count - {count} where id = {id_product}")
                db.commit()
                sql.execute(f"SELECT name FROM PRODUCTS WHERE id = {id_product}")
                name_product = sql.fetchone()
                order_list += f'Товар: "{name_product[0]}", количество: {count}.\n'
            order_id = rows[0][0]
            sql.execute(f"INSERT INTO status (user_id, order_id, order_status) VALUES ('{user_id}', '{order_id}', {0})")
            db.commit()
            sql.execute(f"DELETE FROM cart WHERE user_id = {user_id}")
            db.commit()
            change_balance()
            bot.send_message(message.chat.id, f'Вы успешно оформили заказ #{order_id} 📦')
            for id in id_seller:
                bot.send_message(id,
                                 f'Пользователь @{user_name} оформил заказ #{order_id} 📧\n \n{order_list}\n'
                                 f'Адрес покупателя: {address} 🚛\nИтоговая сумма заказа: {final_sum} 💳')

        if final_sum <= balance: #Проверка хватает ли у пользователя средств для совершения покупки
            address_new = bot.send_message(call.message.chat.id, f'Введите адрес доставки (город, улица, дом, квартира):')
            bot.register_next_step_handler(address_new, get_cart)
        else:
            user_id = call.message.chat.id
            sql.execute(f"DELETE FROM cart WHERE user_id = {user_id}")
            db.commit()
            bot.send_message(call.message.chat.id, f'На вашем счету недостаточно средств. Не хватает {final_sum - balance}')



    elif call.data == "cancel_cart":
        user_id = call.message.chat.id
        sql.execute(f"DELETE FROM cart WHERE user_id = {user_id}")
        db.commit()
        bot.send_message(call.message.chat.id, f'Ваша корзина удалена.')

    elif call.data == "publish_otz":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                 text='✅ Отзыв опубликован!')
        for id in id_seller:
            bot.send_message(id, f'Опубликован новый отзыв: {call.message.text} 💬')

    elif call.data == "decline_otz":
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = '❌ Отзыв отклонён')

bot.polling(none_stop=True)



