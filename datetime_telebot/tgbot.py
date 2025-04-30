import telebot
import datetime
import sqlite3

def create():
    db = sqlite3.connect("datetime_telebot.db")
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS schedulary (days TEXT, num INTEGER PRIMARY KEY)""")
    db.close()

def get(num):
    db = sqlite3.connect("datetime_telebot.db")
    cur = db.cursor()
    cur.execute(f"""SELECT * FROM schedulary WHERE num == (?) """, (num,))
    result = cur.fetchall()
    return result

TOKEN = '6120866869:AAHhx1yCQs3MjBiLEaYFwyiS8nYfTxhAFl0'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(chat_id=message.chat.id, text="Hi, it`s your diary!")
    create()

@bot.message_handler(commands=["send_today"])
def send_today(message):
    day = get(datetime.datetime.now().weekday())
    bot.send_message(chat_id=message.chat.id, text=f'{day[0][0]}')

@bot.message_handler(commands=["twod"])
def twod(message):
    days = []
    today = datetime.datetime.now().weekday()
    temp_time = today
    for i in range(1, 3):

        if temp_time + 1 <= 6:
            day = get(temp_time + 1)
            temp_time += 1
        else:
            temp_time -= 6
            day = get(temp_time)
        days.append(day[0][0])
    bot.send_message(chat_id=message.chat.id, text=f'{" \n".join(days)}')

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, text=f"{message}")

bot.polling(non_stop=True)