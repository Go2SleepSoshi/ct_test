import telebot
import config
import re
import sqlite3
import datetime
import quest_tree

#Анкета:
#1.ФИО
#2.Адрес регистрации
#3.Дата покупки
#4.Номер заказа
#5.Фото товара
#6.Категория товара
#7. Дата получения товара


bot = telebot.TeleBot(config.token)
order_dict = {} #словарь для обработки анкеты
user_tree_state = {} #словарь, хранящий положение пользователя в дереве ответов
questions = quest_tree.questoins #файл с деревом ответов

class DBConnect:
    """
    Класс для подключения к базе данных и взаимодействия с ней.
    Методы класса: select_query, update_query, insert_query, close
    """

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_query(self, what, where):
        with self.connection:
            return self.cursor.execute("SELECT {} FROM {}".format(what, where)).fetchall()

    def update_query(self, table, what, value, where, condition):
        with self.connection:
            self.cursor.execute("UPDATE {} SET {}=(?) WHERE {}=(?)".format(table, what, where),(value,condition)).fetchall()

    def insert_query(self, table, columns, values):
        with self.connection:
            self.cursor.execute("INSERT INTO {} ({}) VALUES ({});".format(table, columns, values))

    def close(self):
        self.connection.close()


class Order:

    #название категории: [ПП(перечень товаров не подлежащих обмену и возврату), ТСТ(технически сложный товар)]
    cat_info = {'одежда и обувь':[0, 0], 'белье':[1, 0], 'канцтовары':[0, 0], 'бытовая электроника':[1, 0],
                'смартфоны и планшеты': [1, 1], 'аксессуары':[0, 0], 'часы':[1, 1], 'ювелирные изделия':[1, 0],
                'игрушки': [0, 0], 'автомобильные аксессуары':[0, 0], 'автомобильная электроника':[1, 1],
                'парфюмерия и косметика':[1, 0], 'посуда': [1, 0], 'строительные материалы':[1, 0],
                'мебель':[1, 0]
                }

    def __init__(self, user_id):
        self.user = user_id
        self.fio = ''
        self.adress = ''
        self.buy_date = ''
        self.order_num = ''
        self.photo = ''
        self.category = ''
        self.recieve_date = ''

    def save_order(self):
        connection = DBConnect(config.db_name)
        user_db = connection.select_query("id","user WHERE tg_id={}".format(self.user))
        connection.insert_query("order_data", "name, adress, buy_date, order_num, photo_id, category, recieve_date, user_id",
                                """'{fio}', '{adress}', '{buy_date}', '{order_num}', '{photo_id}', '{category}', '{recieve_date}', {user_db}
                                """.format(fio=self.fio, adress=self.adress, buy_date=self.buy_date, order_num=self.order_num, photo_id=self.photo,
                                           category=self.category, recieve_date=self.recieve_date, user_db=user_db[0][0]).rstrip())
        connection.close()

    def get_status(self):
        if self.category in self.cat_info:
            return [self.cat_info[self.category][0], self.cat_info[self.category][1]]
        else:
            return None


class User:
    """
    Класс для взаимодействия с пользователями бота, методы реализуют взаимодействие с бд.
    Методы класса: get_state, set_state, insert_user, check_user, get_recieve_date, get_category_info
    """

    def __init__(self, user_id):
        self.id = user_id
        self.state = 0

    def get_state(self):
        connection = DBConnect(config.db_name)
        state = connection.select_query("user_state","user WHERE tg_id={}".format(self.id))[0][0]
        connection.close()
        return state

    def set_state(self, state):
        connection = DBConnect(config.db_name)
        connection.update_query("user", "user_state", state, "tg_id", self.id)
        connection.close()

    def insert_user(self):
        connection = DBConnect(config.db_name)
        connection.insert_query("user","user_state, tg_id","0, {}".format(self.id))
        connection.close()

    def check_user(self):
        connection = DBConnect(config.db_name)
        check = connection.select_query("user_state", "user WHERE tg_id={}".format(self.id))
        connection.close()
        if check != []:
            return "Exists"
        else:
            return "Not exists"

    def get_recieve_date(self):
        connection = DBConnect(config.db_name)
        date = connection.select_query("recieve_date", "order_data inner join user on user.id = order_data.user_id WHERE user.tg_id={}".format(self.id))[-1][0]
        connection.close()
        return date

    def get_category_info(self):
        connection = DBConnect(config.db_name)
        category = connection.select_query("category", "order_data inner join user on user.id = order_data.user_id WHERE user.tg_id={}".format(self.id))[-1][0]
        connection.close()
        return Order.cat_info[category]

    def set_order_result(self, result):
        connection = DBConnect(config.db_name)
        #connection.update_query("order_data", "order_result", result, "tg_id", self.id)
        connection.close()

#обработчик команды /start, реализует последовательный вызов функций, необходимых для создания анкеты
@bot.message_handler(commands=["start"])
def start_message(message):
    try:
        user = User(message.chat.id)
        order_dict[user.id] = Order(user.id)

        if user.check_user() == "Not exists":
            user.insert_user()

        user.set_state(1)
        bot.send_message(message.chat.id, "Здравствуйте, введите данные для анкеты. Будьте внимательны, введенные данные необходимы для точного ответа на Ваш вопрос!")
        bot.send_message(message.chat.id, "Введите ФИО")
        bot.register_next_step_handler(message, get_fio)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Произошла ошибка, попробуйте ввести команду /start")

def get_fio(message):
    try:
        fio = message.text
        order_dict[message.chat.id].fio = fio
        bot.send_message(message.chat.id, "Введите адрес регистрации")
        bot.register_next_step_handler(message, get_adress)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Произошла ошибка, попробуйте ввести команду /start")

def get_adress(message):
    try:
        adress = message.text
        order_dict[message.chat.id].adress = adress
        bot.send_message(message.chat.id, "Введите дату покупки в формате dd.mm.yyyy")
        bot.register_next_step_handler(message, buy_date)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Произошла ошибка, попробуйте ввести команду /start")

def buy_date(message):
    try:
        if re.match(r"\d\d\.\d\d\.\d\d\d\d", message.text) is None:
            bot.send_message(message.chat.id, "Неверная дата! Введите дату покупки в формате dd.mm.yyyy")
            return bot.register_next_step_handler(message, buy_date)
        date = message.text
        order_dict[message.chat.id].buy_date = date
        bot.send_message(message.chat.id, "Введите номер заказа")
        bot.register_next_step_handler(message, order_num)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Произошла ошибка, попробуйте ввести команду /start")

def order_num(message):
    try:
        if re.search(r'[^\w]', message.text) is not None:
            bot.send_message(message.chat.id, "Введены недопустимые символы, попробуйте снова")
            return bot.register_next_step_handler(message, order_num)
        order = message.text
        order_dict[message.chat.id].order_num = order
        bot.send_message(message.chat.id, "Отправьте фотографию товара")
        bot.register_next_step_handler(message, order_photo)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Произошла ошибка, попробуйте ввести команду /start")

def order_photo(message):
    try:
        #print(message.photo)
        if (message.photo) is None:
            bot.send_message(message.chat.id, "Что-то пошло не так, отправьте фотографию товара")
            return bot.register_next_step_handler(message, order_photo)
        photo = message.photo[0].file_id
        order_dict[message.chat.id].photo = photo
        bot.send_message(message.chat.id, "Введите категорию товара <b>без номера категории</b>",parse_mode="HTML")

        counter = 1
        for key, value in Order.cat_info.items():
            bot.send_message(message.chat.id, "{counter}: {key}".format(counter=counter, key=key))
            counter += 1

        bot.register_next_step_handler(message, order_category)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Произошла ошибка, попробуйте ввести команду /start")

def order_category(message):
    try:
        if message.text.lower().strip() not in Order.cat_info:
            bot.send_message(message.chat.id, "Неверная категория! Введите категорию товара ")
            return bot.register_next_step_handler(message, order_category)
        category = message.text.lower().strip()
        order_dict[message.chat.id].category = category
        bot.send_message(message.chat.id, "Введите дату получения товара")
        bot.register_next_step_handler(message, recieve_date)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Произошла ошибка, попробуйте ввести команду /start")

def recieve_date(message):
    try:
        if re.match(r"\d\d\.\d\d\.\d\d\d\d", message.text) is None:
            bot.send_message(message.chat.id, "Неверная дата! Введите дату получения товара в формате dd.mm.yyyy")
            return bot.register_next_step_handler(message, recieve_date)
        recieved = message.text
        order_dict[message.chat.id].recieve_date = recieved

        bot.send_message(message.chat.id,""" 
        Вы ввели следующие данные:
1.ФИО: {}
2.Адрес регистрации: {}
3.Дата покупки: {}
4.Номер заказа: {}
5.Категория товара: {}
6.Дата получения товара: {}
        """.format(order_dict[message.chat.id].fio, order_dict[message.chat.id].adress, order_dict[message.chat.id].buy_date,
                   order_dict[message.chat.id].order_num, order_dict[message.chat.id].category, order_dict[message.chat.id].recieve_date))

        order_dict[message.chat.id].save_order()
        bot.send_photo(message.chat.id, order_dict[message.chat.id].photo)
        user = User(message.chat.id)
        user.set_state(2)
        del order_dict[message.chat.id]
        bot.send_message(message.chat.id, "Для продолжения взаимодействия используйте команду /continue")
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Произошла ошибка, попробуйте ввести команду /start")

#обработчик команды /continue. Реализует проход по дереву ответов на основе анкеты, хранящейся в бд
@bot.message_handler(commands=["continue"])
def continue_message(message):
    try:
        user = User(message.chat.id)

        #print(user.get_state())
        if user.get_state() != 2:
            bot.send_message(message.chat.id, "У Вас отсутствует анкета, введите /start чтобы создать")
            return

        user_tree_state[user.id] = 'root'

        ans_mkup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        ans_mkup.row('да', 'нет')
        bot.send_message(message.chat.id, questions['root']['text'], reply_markup=ans_mkup)
        bot.register_next_step_handler(message, tree_handler)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Произошла непревиденная ошибка, введите команду /continue чтобы начать сначала")

def tree_handler(message):
    try:
        state = user_tree_state[message.chat.id]

        if message.text == "да":
            #print(questions[state]['r_child'])
            #print(questions['2'])
            cur_state = questions[state]['r_child']

            if questions[cur_state]['make'] == 1:
                days = date_amplitude(message)

                if cur_state == '9':
                    if days >= 7:
                        cur_state = questions[cur_state]['r_child']
                    elif days < 7:
                        cur_state = questions[cur_state]['l_child']

                elif cur_state == '17':
                    if days/365 > 2:
                        cur_state = questions[cur_state]['r_child']
                    elif days/365 <= 2:
                        cur_state = questions[cur_state]['l_child']

                elif cur_state == '23':
                    if User(message.chat.id).get_category_info()[1] == 1:
                        cur_state = questions[cur_state]['r_child']
                    elif User(message.chat.id).get_category_info()[1] == 0:
                        cur_state = questions[cur_state]['l_child']

                elif cur_state == '25':
                    if days >= 15:
                        cur_state = questions[cur_state]['r_child']
                    elif days < 15:
                        cur_state = questions[cur_state]['l_child']

            ans_mkup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            ans_mkup.row('да', 'нет')
            bot.send_message(message.chat.id, questions[cur_state]['text'], reply_markup=ans_mkup)
            user_tree_state[message.chat.id] = cur_state

            if questions[cur_state]['stop'] != 0:
                # Вставить статус окончания в ордер в бд
                # user = User(message.chat.id)
                # user.set_state(3)
                del user_tree_state[message.chat.id]
                return

            return bot.register_next_step_handler(message, tree_handler)

        elif message.text == "нет":
            cur_state = questions[state]['l_child']

            if questions[cur_state]['make'] == 1:
                days = date_amplitude(message)

                if cur_state == '3':
                    if User(message.chat.id).get_category_info()[0] == 1:
                        cur_state = questions[cur_state]['r_child']
                    elif User(message.chat.id).get_category_info()[0] == 0:
                        cur_state = questions[cur_state]['l_child']

                elif cur_state == '7':
                    if days >= 15:
                        cur_state = questions[cur_state]['r_child']
                    elif days < 15:
                        cur_state = questions[cur_state]['l_child']

            ans_mkup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            ans_mkup.row('да', 'нет')
            bot.send_message(message.chat.id, questions[cur_state]['text'], reply_markup=ans_mkup)
            user_tree_state[message.chat.id] = cur_state

            if questions[cur_state]['stop'] != 0:
                # Вставить статус окончания в ордер в бд
                #user = User(message.chat.id)
                #user.set_state(3)
                del user_tree_state[message.chat.id]
                return

            return bot.register_next_step_handler(message, tree_handler)

        else:
            bot.send_message(message.chat.id, "Введен некорректный ответ, принимаются варианты \"да/нет\"")
            return bot.register_next_step_handler(message, tree_handler)

    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Произошла непревиденная ошибка, введите команду /continue чтобы начать сначала")

def date_amplitude(message):
    try:
        now = datetime.datetime.now()
        user_date = User(message.chat.id).get_recieve_date().split('.')
        formated_date = datetime.datetime(int(user_date[2]), int(user_date[1]), int(user_date[0]))
        amplitude = now - formated_date
        return amplitude.days
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Произошла непревиденная ошибка, введите команду /continue чтобы начать сначала")

@bot.message_handler(commands=["help"])
def help_message(message):
    bot.send_message(message.chat.id,
                     """Для получения ответа на Ваш вопрос требуется выполнить следующие действия:
                     
1. Заполненить анкету
2. Ответить на вопросы бота
                     
Команда /start используется для начала заполнения анкеты. 
Если анкета была заполнена некорректно, повторно используйте команду /start для рестарта.
                     
Команда /continue доступна после того, как Вы заполнили анкету.
Эта команда начинает диалог с ботом.
                     
Команда /help выводит это сообщение.
                     """)

@bot.message_handler(content_types=["text"])
def echo_message(message):
    bot.send_message(message.chat.id, "Для взаимодействия с ботом используйте команды /start или /continue, для получения справки введите /help")

if __name__ == '__main__':
    bot.polling(none_stop=True)