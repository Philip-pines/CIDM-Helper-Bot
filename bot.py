import sys
import telebot
import mysql.connector
from mysql.connector import connect, errorcode
from telebot import types
from datetime import datetime
import pyodbc
import datetime
import pyqrcode


bot = telebot.TeleBot([TOKEN])
group_cawresd =  {chat_ID}
group_talresd = {chat_ID}
group_resv = {chat_ID}
group_cancel = {chat_ID}
group_caw = {chat_ID}
group_asc = {chat_ID}

try:
    
    db = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server={server};"
                      "Database={db};"
                      "uid={username};"
                      "pwd={password};"
)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
    sys.exit()
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
    sys.exit()
  else:
    print(err)
    sys.exit()


cursor = db.cursor()

user_data = {}

class User:
    def __init__(self, first_name):
        self.first_name = first_name
        self.last_name = ''
        self.reservation = ''
        self.bu = ''
        self.shift = ''
        self.cancel = ''
        self.claim = ''
        self.no = ''

@bot.message_handler(commands=['qr_code'])
def qr_code_handler(message):    
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        sent = bot.send_message(message.chat.id, "Send Text or Url")
        bot.register_next_step_handler(sent, qrcode)
    except Exception as e:
        bot.reply_to(message, 'Error. Please try again.')

def qrcode(message):
    try:
        url=pyqrcode.create(message.text)
        url.png('qrcode.png',scale=15)
        bot.send_chat_action(message.chat.id, 'upload_document')
        bot.send_document(message.chat.id,open('qrcode.png','rb' ))
    except Exception as e:
        bot.reply_to(message, 'Error. Please try again.')

@bot.message_handler(commands=['cawresident'])
def creservation(message):
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Breakfast', 'Lunch', 'Dinner')

        msg = bot.send_message(message.chat.id, 'What kind of meal?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_cresident_step)
    except Exception as e:
        bot.reply_to(message, 'Error. Please try again.')

def process_cresident_step(message):
    try:
        user_id = message.from_user.id
        reservation = message.text
        meal = 'For pick up'
        bu = 'CAWIT RESIDENCE'
        CURRENT_TIMESTAMP = datetime.datetime.now()

        sql = "SELECT * FROM users WHERE telegram_user_id = {0}".format(user_id)
        cursor.execute(sql)
        existsUser = cursor.fetchone()
        print(existsUser)

        if (existsUser == None):

               sql = 'INSERT INTO users(first_name, last_name, telegram_user_id) VALUES(?, ?, ?);' 
               val = message.from_user.first_name, message.from_user.last_name, user_id    
               cursor.execute(sql, val)
               db.commit()   

        sql = 'INSERT INTO mealresv(first_name, last_name, reservation, bu, shift, date_time) VALUES(?,?,?,?,?,?);'
        val = message.from_user.first_name, message.from_user.last_name, meal, reservation, bu, CURRENT_TIMESTAMP
        cursor.execute(sql, val)
        db.commit()
        user_data.clear()

        bot.send_message(message.chat.id, 'Your input has been successfully logged!')

        if (bu == "CAWIT RESIDENCE"):
                if (reservation == "Breakfast"):
                    bot.send_message(group_cawresd, message.from_user.first_name + ' ' + message.from_user.last_name + ", a " + bu + " occupant, reserved meal for breakfast." )
                    bot.send_video(message.chat.id, "https://i.giphy.com/1LweXxLwVT0J2.gif")
                elif (reservation == "Lunch"):
                    bot.send_message(group_cawresd, message.from_user.first_name + ' ' + message.from_user.last_name + ", a " + bu + " occupant, reserved meal for lunch.")
                    bot.send_video(message.chat.id, "https://i.giphy.com/O4AncsVUvSgWQ.gif")
                elif (reservation == "Dinner"):
                    bot.send_message(group_cawresd, message.from_user.first_name + ' ' + message.from_user.last_name + ", a " + bu + " occupant, reserved meal for dinner.")
                    bot.send_video(message.chat.id, "https://i.giphy.com/Up6ZK08iwIyBy.gif")
                else:
                    bot.send_message(message.chat.id, "Please use the predefined keyboard.")
                    bot.send_message(message.chat.id, "Please /start again.")     
        else:
                bot.send_message(message.chat.id, "Please use the predefined keyboard.")
                bot.send_message(message.chat.id, "Please /start again.")

    except Exception as e:
        bot.reply_to(message, 'Error. Please try again.')

@bot.message_handler(commands=['talresident'])
def treservation(message):
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Breakfast', 'Lunch', 'Dinner')

        msg = bot.send_message(message.chat.id, 'What kind of meal?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_tresident_step)
    except Exception as e:
        bot.reply_to(message, 'Error. Please try again.')

def process_tresident_step(message):
    try:
        user_id = message.from_user.id
        reservation = message.text
        meal = 'For pick up'
        bu = 'TAL RESIDENCE'
        CURRENT_TIMESTAMP = datetime.datetime.now()

        sql = "SELECT * FROM users WHERE telegram_user_id = {0}".format(user_id)
        cursor.execute(sql)
        existsUser = cursor.fetchone()
        print(existsUser)

        if (existsUser == None):

               sql = 'INSERT INTO users(first_name, last_name, telegram_user_id) VALUES(?, ?, ?);' 
               val = message.from_user.first_name, message.from_user.last_name, user_id    
               cursor.execute(sql, val)
               db.commit()   

        sql = 'INSERT INTO mealresv(first_name, last_name, reservation, bu, shift, date_time) VALUES(?,?,?,?,?,?);'
        val = message.from_user.first_name, message.from_user.last_name, meal, reservation, bu, CURRENT_TIMESTAMP
        cursor.execute(sql, val)
        db.commit()
        user_data.clear()

        bot.send_message(message.chat.id, 'Your input has been successfully logged!')

        if (bu == "TAL RESIDENCE"):
                if (reservation == "Breakfast"):
                    bot.send_message(group_talresd, message.from_user.first_name + ' ' + message.from_user.last_name + ", a " + bu + " occupant, reserved meal for breakfast." )
                    bot.send_video(message.chat.id, "https://i.giphy.com/1LweXxLwVT0J2.gif")
                elif (reservation == "Lunch"):
                    bot.send_message(group_talresd, message.from_user.first_name + ' ' + message.from_user.last_name + ", a " + bu + " occupant, reserved meal for lunch.")
                    bot.send_video(message.chat.id, "https://i.giphy.com/O4AncsVUvSgWQ.gif")
                elif (reservation == "Dinner"):
                    bot.send_message(group_talresd, message.from_user.first_name + ' ' + message.from_user.last_name + ", a " + bu + " occupant, reserved meal for dinner.")
                    bot.send_video(message.chat.id, "https://i.giphy.com/Up6ZK08iwIyBy.gif")
                else:
                    bot.send_message(message.chat.id, "Please use the predefined keyboard.")
                    bot.send_message(message.chat.id, "Please /start again.")     
        else:
                bot.send_message(message.chat.id, "Please use the predefined keyboard.")
                bot.send_message(message.chat.id, "Please /start again.")

    except Exception as e:
        bot.reply_to(message, 'Error. Please try again.')

@bot.message_handler(commands=['ascresident'])
def areservation(message):
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Breakfast', 'Lunch', 'Dinner')

        msg = bot.send_message(message.chat.id, 'What kind of meal?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_aresident_step)
    except Exception as e:
        bot.reply_to(message, 'Error. Please try again.')

def process_aresident_step(message):
    try:
        user_id = message.from_user.id
        reservation = message.text
        meal = 'For pick up'
        bu = 'ASC RESIDENCE'
        CURRENT_TIMESTAMP = datetime.datetime.now()

        sql = "SELECT * FROM users WHERE telegram_user_id = {0}".format(user_id)
        cursor.execute(sql)
        existsUser = cursor.fetchone()
        print(existsUser)

        if (existsUser == None):

               sql = 'INSERT INTO users(first_name, last_name, telegram_user_id) VALUES(?, ?, ?);' 
               val = message.from_user.first_name, message.from_user.last_name, user_id    
               cursor.execute(sql, val)
               db.commit()   

        sql = 'INSERT INTO mealresv(first_name, last_name, reservation, bu, shift, date_time) VALUES(?,?,?,?,?,?);'
        val = message.from_user.first_name, message.from_user.last_name, meal, reservation, bu, CURRENT_TIMESTAMP
        cursor.execute(sql, val)
        db.commit()
        user_data.clear()

        bot.send_message(message.chat.id, 'Your input has been successfully logged!')

        if (bu == "ASC RESIDENCE"):
                if (reservation == "Breakfast"):
                    bot.send_message(group_asc, message.from_user.first_name + ' ' + message.from_user.last_name + ", an " + bu + " occupant, reserved meal for breakfast." )
                    bot.send_video(message.chat.id, "https://i.giphy.com/1LweXxLwVT0J2.gif")
                elif (reservation == "Lunch"):
                    bot.send_message(group_asc, message.from_user.first_name + ' ' + message.from_user.last_name + ", an " + bu + " occupant, reserved meal for lunch.")
                    bot.send_video(message.chat.id, "https://i.giphy.com/O4AncsVUvSgWQ.gif")
                elif (reservation == "Dinner"):
                    bot.send_message(group_asc, message.from_user.first_name + ' ' + message.from_user.last_name + ", an " + bu + " occupant, reserved meal for dinner.")
                    bot.send_video(message.chat.id, "https://i.giphy.com/Up6ZK08iwIyBy.gif")
                else:
                    bot.send_message(message.chat.id, "Please use the predefined keyboard.")
                    bot.send_message(message.chat.id, "Please /start again.")     
        else:
                bot.send_message(message.chat.id, "Please use the predefined keyboard.")
                bot.send_message(message.chat.id, "Please /start again.")

    except Exception as e:
        bot.reply_to(message, 'Error. Please try again.')


@bot.message_handler(commands=['today'])
def today(message):
    try:
        cursor.execute('SELECT first_name FROM mealresv WHERE date_time >= CAST(GETDATE() AS DATE);')
        for x in cursor:
            bot.reply_to(message, x)
    except Exception as e:
        bot.reply_to(message, 'Error. Please try again.')

@bot.message_handler(commands=['no'])
def no(message):
    try:
        bot.reply_to(message, message.from_user.first_name + " does not want to reserve meal.")
        bot.send_message(group_resv, message.from_user.first_name + ' ' + message.from_user.last_name + " does not want meal reservation.")
    except Exception as e:
        bot.reply_to(message, 'Error. Please try again.')

@bot.message_handler(commands=['claim'])
def send_claim(message):
        msg = bot.send_message(message.chat.id, "Enter first name")
        bot.register_next_step_handler(msg, process_sfirstname_step)

def process_sfirstname_step(message):
    try:
        user_id = message.from_user.id
        user_data[user_id] = User(message.text)
        msg = bot.send_message(message.chat.id, 'Enter last name')
        bot.register_next_step_handler(msg, process_slastname_step)
    except Exception as e:
        bot.reply_to(message, 'Error. Please try again.')

def process_slastname_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.last_name = message.text

        msg = bot.send_message(message.chat.id, 'Enter \"month\" and \"day\" when the meal is reserved.')
        bot.register_next_step_handler(msg, process_monthday_step)
    except Exception as e:
        bot.reply_to(message, 'Error. Please try again.')

def process_monthday_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.monthday = message.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Breakfast', 'Lunch', 'Dinner')

        msg = bot.send_message(message.chat.id, 'What type of meal?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_meal_step)
    except Exception as e:
        bot.reply_to(message, 'Error. Please try again.')

def process_meal_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.meal = message.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('claimed', 'not claimed')

        msg = bot.send_message(message.chat.id, 'What type of meal?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_claim_step)
    except Exception as e:
        bot.reply_to(message, 'Error. Please try again.')

def process_claim_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.claim = message.text
        # timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        CURRENT_TIMESTAMP = datetime.datetime.now()

        sql = "SELECT * FROM users WHERE telegram_user_id = {0}".format(user_id)
        cursor.execute(sql)
        existsUser = cursor.fetchone()
        print(existsUser)

        if (existsUser == None):
               sql = 'INSERT INTO users(first_name, last_name, telegram_user_id) VALUES(?, ?, ?);' 
               val = message.from_user.first_name, message.from_user.last_name, user_id    
               cursor.execute(sql, val)
               db.commit()  

        sql = 'INSERT INTO claim(first_name, last_name, month_day, meal, claim, date_time) VALUES(?,?,?,?,?,?);'
        val = user.first_name, user.last_name, user.monthday, user.meal, user.claim, CURRENT_TIMESTAMP
        cursor.execute(sql, val)
        db.commit()
        user_data.clear()

        bot.send_message(message.chat.id, 'Your input has been successfully logged!')
        bot.send_message(group_cancel, user.first_name + ' ' + user.last_name + " has " + user.claim + " their " + user.meal + ".")

        # photo = open('img/sad.jpg', 'rb')
        bot.send_video(message.chat.id, "https://i.giphy.com/9JtaAvOgQUNQiobxyW.gif")
        # photo.close()
    except Exception as e:
        bot.reply_to(message, 'Error. Please try again.')

@bot.message_handler(commands=['cancel'])
def send_cancel(message):
        msg = bot.send_message(message.chat.id, "Enter first name")
        bot.register_next_step_handler(msg, process_cfirstname_step)

def process_cfirstname_step(message):
    try:
        user_id = message.from_user.id
        user_data[user_id] = User(message.text)
        msg = bot.send_message(message.chat.id, 'Enter last name')
        bot.register_next_step_handler(msg, process_clastname_step)
    except Exception as e:
        bot.reply_to(message, 'Error. Please try again.')

def process_clastname_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.last_name = message.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Cancel')

        msg = bot.send_message(message.chat.id, 'Would you like to cancel your meal?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_cancel_step)
    except Exception as e:
        bot.reply_to(message, 'Error. Please try again.')

def process_cancel_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.shift = message.text
        # timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # CURRENT_TIMESTAMP = datetime.datetime.now()

        sql = "SELECT * FROM users WHERE telegram_user_id = {0}".format(user_id)
        cursor.execute(sql)
        existsUser = cursor.fetchone()
        print(existsUser)

        if (existsUser == None):
               sql = 'INSERT INTO users(first_name, last_name, telegram_user_id) VALUES(?, ?, ?);' 
               val = message.from_user.first_name, message.from_user.last_name, user_id    
               cursor.execute(sql, val)
               db.commit()   

        # sql = 'INSERT INTO cancelled(first_name, last_name, date_time) VALUES(?,?,?);'
        sql = 'DELETE FROM mealresv WHERE(first_name = ? AND last_name = ? AND date_time >= CAST(GETDATE() AS DATE));'
        val = user.first_name, user.last_name
        cursor.execute(sql, val)
        db.commit()
        user_data.clear()

        bot.send_message(message.chat.id, 'Your input has been successfully logged!')
        bot.send_message(group_cancel, user.first_name + ' ' + user.last_name + " cancelled their meal.")

        photo = open('img/sad.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)
        photo.close()
    except Exception as e:
        bot.reply_to(message, 'Error. Please try again.')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
        bot.send_message(message.chat.id, "Hi! I can help you create meal reservations.\n\nPlease use one of the following commands:\n\nMeal reservation? Press \"/eat\"\nMeal cancellation? Press \"/cancel\"\n\nFor canteen users:\nPlease press \"/claim\" to report if a user hasn't claimed a meal reservation.")
        bot.send_message(message.chat.id, "For CAWIT RESIDENTS, please use \"/cawresident\"\nFor TAL RESIDENTS, please use \"/talresident\"\nFor ASC RESIDENTS, please use \"/ascresident\"")
        bot.send_message(message.chat.id, "QR code generation for general purpose? use \"/qr_code\"")

@bot.message_handler(commands=['eat'])
def send_welcome(message):
        msg = bot.send_message(message.chat.id, "Enter first name")
        bot.register_next_step_handler(msg, process_firstname_step)

def process_firstname_step(message):
    try:
        user_id = message.from_user.id
        user_data[user_id] = User(message.text)
        msg = bot.send_message(message.chat.id, 'Enter last name')
        bot.register_next_step_handler(msg, process_lastname_step)
    except Exception as e:
        bot.reply_to(message, 'Error. Please try again.')

def process_lastname_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.last_name = message.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('For pick up', 'Canteen', 'HQ')

        msg = bot.send_message(message.chat.id, 'Where would you like to eat your meal?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_reservation_step)
    except Exception as e:
        bot.reply_to(message, 'Error. Please try again.')

def process_reservation_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.reservation = message.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Ayala', 'Cawit', 'Talisayan')

        msg = bot.send_message(message.chat.id, 'What BU?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_bu_step)
    except Exception as e:
        bot.reply_to(message, 'Error. Please try again.')

def process_bu_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.bu = message.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Night Shift', 'Day Shift')

        msg = bot.send_message(message.chat.id, 'What Shift?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_shift_step)
    except Exception as e:
        bot.reply_to(message, 'Error. Please try again.')

def process_shift_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.shift = message.text
        # timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        CURRENT_TIMESTAMP = datetime.datetime.now()

        sql = "SELECT * FROM users WHERE telegram_user_id = {0}".format(user_id)
        cursor.execute(sql)
        existsUser = cursor.fetchone()
        print(existsUser)

        if (existsUser == None):
            #    sql = "INSERT INTO users (first_name, last_name, telegram_user_id) \
            #                       VALUES (%s, %s, %s)"
            #    val = (message.from_user.first_name, message.from_user.last_name, user_id)
            #    cursor.execute(sql, val)
               sql = 'INSERT INTO users(first_name, last_name, telegram_user_id) VALUES(?, ?, ?);' 
               val = message.from_user.first_name, message.from_user.last_name, user_id    
               cursor.execute(sql, val)
               db.commit()   

        # sql = "INSERT INTO mealresv (first_name, last_name, reservation, bu, shift, date_time) \
        #                               VALUES (%s, %s, %s, %s, %s, %s)"
        # val = (user.first_name, user.last_name, user.reservation, user.bu, user.shift, timestamp)
        # # val = (user.first_name, user.last_name, user.reservation, user.bu, user.shift, CURRENT_TIMESTAMP)
        # cursor.execute(sql, val)
        # db.commit()
        # user_data.clear()
        sql = 'INSERT INTO mealresv(first_name, last_name, reservation, bu, shift, date_time) VALUES(?,?,?,?,?,?);'
        val = user.first_name, user.last_name, user.reservation, user.bu, user.shift, CURRENT_TIMESTAMP
        cursor.execute(sql, val)
        db.commit()
        user_data.clear()

        bot.send_message(message.chat.id, 'Your input has been successfully logged!')
        if (user.bu == "Ayala"):
                if (user.reservation == "HQ"):
                    bot.send_message(group_asc, user.first_name + ' ' + user.last_name + " wants to have their meal delivered to HQ for " + user.shift + " at " + user.bu)
                    bot.send_video(message.chat.id, "https://i.giphy.com/xT0BKhSthOLHYzw640.gif")
                elif (user.reservation == "For pick up"):
                    bot.send_message(group_asc, user.first_name + ' ' + user.last_name + " wants to pick up their meal for " + user.shift + " at " + user.bu)
                    bot.send_video(message.chat.id, "https://i.giphy.com/9JtaAvOgQUNQiobxyW.gif")
                elif (user.reservation == "Canteen"):
                    bot.send_message(group_asc, user.first_name + ' ' + user.last_name + " wants to eat their meal in canteen for " + user.shift + " at " + user.bu)
                    bot.send_video(message.chat.id, "https://i.giphy.com/O4AncsVUvSgWQ.gif")
                else:
                    bot.send_message(message.chat.id, "Please use the predefined keyboard.")
                    bot.send_message(message.chat.id, "Please /start again.")    
        elif (user.bu == "Cawit"):
                if (user.reservation == "HQ"):
                    bot.send_message(group_caw, user.first_name + ' ' + user.last_name + " wants to have their meal delivered to HQ for " + user.shift + " at " + user.bu)
                    bot.send_video(message.chat.id, "https://i.giphy.com/xT0BKhSthOLHYzw640.gif")
                elif (user.reservation == "For pick up"):
                    bot.send_message(group_caw, user.first_name + ' ' + user.last_name + " wants to pick up their meal for " + user.shift + " at " + user.bu)
                    bot.send_video(message.chat.id, "https://i.giphy.com/9JtaAvOgQUNQiobxyW.gif")
                elif (user.reservation == "Canteen"):
                    bot.send_message(group_caw, user.first_name + ' ' + user.last_name + " wants to eat their meal in canteen for " + user.shift + " at " + user.bu)
                    bot.send_video(message.chat.id, "https://i.giphy.com/O4AncsVUvSgWQ.gif")
                else:
                    bot.send_message(message.chat.id, "Please use the predefined keyboard.")
                    bot.send_message(message.chat.id, "Please /start again.")    
        elif (user.bu == "Talisayan"):
                if (user.reservation == "HQ"):
                    bot.send_message(group_resv, user.first_name + ' ' + user.last_name + " wants to have their meal delivered to HQ for " + user.shift + " at " + user.bu)
                    bot.send_video(message.chat.id, "https://i.giphy.com/xT0BKhSthOLHYzw640.gif")
                elif (user.reservation == "For pick up"):
                    bot.send_message(group_resv, user.first_name + ' ' + user.last_name + " wants to pick up their meal for " + user.shift + " at " + user.bu)
                    bot.send_video(message.chat.id, "https://i.giphy.com/9JtaAvOgQUNQiobxyW.gif")
                elif (user.reservation == "Canteen"):
                    bot.send_message(group_resv, user.first_name + ' ' + user.last_name + " wants to eat their meal in canteen for " + user.shift + " at " + user.bu)
                    bot.send_video(message.chat.id, "https://i.giphy.com/O4AncsVUvSgWQ.gif")
                else:
                    bot.send_message(message.chat.id, "Please use the predefined keyboard.")
                    bot.send_message(message.chat.id, "Please /start again.")                 
        else:
                bot.send_message(message.chat.id, "Please use the predefined keyboard.")
                bot.send_message(message.chat.id, "Please /start again.")

    except Exception as e:
        bot.reply_to(message, 'Error. Please try again.')

@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "I don't understand \"" + m.text + "\"\n\nMaybe try the help page at \"/help\"\nMeal reservation? Press \"/eat\"\nMeal reservation cancellation? Press \"/cancel\"\nReport unclaimed meal? Press \"/claim\"")
    bot.send_message(m.chat.id, "For CAWIT RESIDENTS, please press \"/cawresident\"\nFor TAL RESIDENTS, please press \"/talresident\"\nFor ASC RESIDENTS, please press \"/ascresident\"")
    bot.send_message(m.chat.id, "QR code generation for general purpose? use \"/qr_code\"")

bot.enable_save_next_step_handlers(delay=3)

bot.load_next_step_handlers()

if __name__=='__main__':
    bot.polling(none_stop=True)
