import telebot
import sqlite3
import config as cfg
import json

client = telebot.TeleBot(cfg.token)

connection = sqlite3.connect('notes.db')
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS notes(
        uid INT,
        nid INT,
        message TEXT
)""")

connection.commit()


@client.message_handler(commands=['add_note', 'an'])
def add_note(message):
    content = message.text.split()
    nid = int(content[1])
    text = str(content[2])
    print('[LOG] Used command `add_note`')
    loc_connection = sqlite3.connect('notes.db')
    loc_cursor = loc_connection.cursor()
    loc_cursor.execute(f"SELECT * FROM notes WHERE uid={message.chat.id}")
    msg = loc_cursor.fetchall()
    trigger = 1
    for i in msg:
        if i[1] == nid:
            trigger = 0
            client.send_message(message.chat.id, 'Запись с таким ID уже существует')
            break
    if trigger:
        loc_cursor.execute(f"INSERT INTO notes (uid, nid, message) VALUES ({message.chat.id}, {nid}, '{text}')")
        loc_connection.commit()
        client.send_message(message.chat.id, 'Запись успешно добавлена в журнал')


@client.message_handler(commands=['view_note', 'vn'])
def add_note(message):
    print('[LOG] Used command `view_note`')
    loc_connection = sqlite3.connect('notes.db')
    loc_cursor = loc_connection.cursor()
    loc_cursor.execute(f"SELECT * FROM notes WHERE uid={message.chat.id}")
    msg = loc_cursor.fetchall()
    ans1 = []
    ans2 = []
    for i in msg:
        ans1.append(str(i[1]))
        print(i[1])
        ans2.append(str(i[2]))
    ans = ''
    for i in range(len(msg)):
        ans += str(ans1[i])
        ans += ': '
        ans += ans2[i]
        ans += '\n'
    if len(msg) == 0:
        ans = 'Записей пока нет...'
    client.send_message(message.chat.id, 'Лист записей:\n'
                                         f'{ans}')


@client.message_handler(commands=['delete_note', 'dn'])
def delete_note(message):
    content = message.text.split()
    nid = int(content[1])
    print('[LOG] Used command `delete_note`')
    loc_connection = sqlite3.connect('notes.db')
    loc_cursor = loc_connection.cursor()
    loc_cursor.execute(f"SELECT * FROM notes WHERE uid={message.chat.id}")
    msg = loc_cursor.fetchall()
    trigger = 0
    for i in msg:
        if i[1] == nid:
            trigger = 1
            loc_cursor.execute(f"DELETE FROM notes WHERE uid={message.chat.id} AND nid={nid}")
            client.send_message(message.chat.id, 'Запись успешно удалена')
            loc_connection.commit()
    if not trigger:
        client.send_message(message.chat.id, 'Запись с таким ID не существует')


client.polling(none_stop=True, interval=0)
