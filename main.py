import telebot
import botInfo
import random
import time
import threading




botInfo.con

bot = telebot.TeleBot(botInfo.token)

keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard.row('/reg')

menuKeyboard = telebot.types.ReplyKeyboardMarkup(True, True)
menuKeyboard.row('Баланс', 'Заработать')
menuKeyboard.row('Магазин', 'Мой профиль')

endKeyboard = telebot.types.ReplyKeyboardMarkup(True, True)
endKeyboard.row('Закончить')

clearKeyboard = telebot.types.InlineKeyboardMarkup()
item1 = telebot.types.InlineKeyboardButton('Да', callback_data='clearYes')
item2 = telebot.types.InlineKeyboardButton('Нет', callback_data='clearNo')
clearKeyboard.add(item1, item2)

earnKeyboard = telebot.types.InlineKeyboardMarkup()
item1 = telebot.types.InlineKeyboardButton('Математика', callback_data='math')
item2 = telebot.types.InlineKeyboardButton('<- Меню', callback_data='menu')
earnKeyboard.add(item1)
earnKeyboard.add(item2)

mathLevelKeyboard = telebot.types.InlineKeyboardMarkup()
item1 = telebot.types.InlineKeyboardButton('1', callback_data='level1')
item2 = telebot.types.InlineKeyboardButton('2', callback_data='level2')
item3 = telebot.types.InlineKeyboardButton('3', callback_data='level3')
item4 = telebot.types.InlineKeyboardButton('<- Меню', callback_data='menu')
mathLevelKeyboard.add(item1, item2, item3)
mathLevelKeyboard.add(item4)

shopKeyboard = telebot.types.InlineKeyboardMarkup()
item1 = telebot.types.InlineKeyboardButton('Майнинг ферма - 500 RUB', callback_data='shopMining')
item2 = telebot.types.InlineKeyboardButton('Шаурмешная - 1000 RUB', callback_data='shopShawa')
item3 = telebot.types.InlineKeyboardButton('Автомойка - 2500 RUB', callback_data='shopMoika')
item4 = telebot.types.InlineKeyboardButton('<- Меню', callback_data='menu')
shopKeyboard.add(item1)
shopKeyboard.add(item2)
shopKeyboard.add(item3)
shopKeyboard.add(item4)

vivodKeyboard = telebot.types.InlineKeyboardMarkup()
item1 = telebot.types.InlineKeyboardButton('Вывести деньги с бизнесов', callback_data='vivod')
item2 = telebot.types.InlineKeyboardButton('<- Меню', callback_data='menu')
vivodKeyboard.add(item1)
vivodKeyboard.add(item2)


def test():
    try:
        rows = botInfo.cur.execute("SELECT * FROM game").fetchall()
        for row in rows:
            user = int(row[0])
            money = int(row[4])
            biz1 = int(row[5])
            biz2 = int(row[6])
            biz3 = int(row[7])
            print(biz1)
            print(user)
            sum = biz1*2 + biz2*4 + biz3*8
            botInfo.cur.execute(f"UPDATE 'game' SET 'bizMoney' = '{money}' + '{sum}' WHERE id = {user}")
            botInfo.con.commit()
        timer.run()
    except Exception as e:
        timer.run()
        print(repr(e))

timer = threading.Timer(60.0, test)
timer.start()

def math(level, userId):
    global answer
    if level == 1:
        a = random.randint(0, 100)
        b = random.randint(0, 100)
        c = random.randint(0, 10)
        botInfo.cur.execute(f"UPDATE game SET answer = {a+b*c} WHERE id = {userId}")
        botInfo.cur.execute(f"UPDATE game SET lvl = {1} WHERE id = {userId}")
        bot.send_message(userId, 'Сколько будет: ' + str(a) + '+' + str(b) + '*' + str(c) + "?")
        return int(a+b*c)
    if level == 2:
        a = random.randint(0, 1000)
        b = random.randint(0, 1000)
        c = random.randint(0, 100)
        botInfo.cur.execute(f"UPDATE game SET answer = {a+b*c} WHERE id = {userId}")
        botInfo.cur.execute(f"UPDATE game SET lvl = {2} WHERE id = {userId}")
        bot.send_message(userId, 'Сколько будет: ' + str(a) + '+' + str(b) + '*' + str(c) + "?")
        return int(a + b * c)
    if level == 3:
        a = random.randint(0, 10000)
        b = random.randint(0, 10000)
        c = random.randint(0, 1000)
        botInfo.cur.execute(f"UPDATE game SET answer = {a+b*c} WHERE id = {userId}")
        botInfo.cur.execute(f"UPDATE game SET lvl = {3} WHERE id = {userId}")
        bot.send_message(userId, 'Сколько будет: ' + str(a) + '+' + str(b) + '*' + str(c) + "?")
        return int(a + b * c)
    if level == 4:
        bot.send_message(userId, 'Это правильный ответ! + 10 RUB', reply_markup=endKeyboard)
        mathComplete(10, userId)
        math(1, userId)
    if level == 5:
        bot.send_message(userId, 'Это правильный ответ! + 20 RUB', reply_markup=endKeyboard)
        mathComplete(20, userId)
        math(2, userId)
    if level == 6:
        bot.send_message(userId, 'Это правильный ответ! + 30 RUB', reply_markup=endKeyboard)
        mathComplete(30, userId)
        math(3, userId)

def mathComplete(money, userId):
    botInfo.cur.execute(f"UPDATE `game` SET `money` = `money` + {money} WHERE id={userId}")
    botInfo.con.commit()

def balance(userId):
    bal = botInfo.cur.execute(f"SELECT money FROM game WHERE id = {userId}").fetchone()[0]
    return bal

def testUserId(userID, reTest):
    test = False
    rows = botInfo.cur.execute("SELECT * FROM 'game'").fetchall()
    for row in rows:
        if userID == row[0]:
            test = True
    if reTest:
        if test:
            return True
        if test == False:
            return False
    if reTest == False:
        if test:
            return 'Вы уже зарегестрированы, хотите начать сначала?', clearKeyboard
        if test == False:
            rows = botInfo.cur.execute("SELECT * FROM 'game'").fetchall()
            for row in rows:
                print(row)
            botInfo.cur.execute(f"INSERT INTO 'game' VALUES ('{userID}','{0}', '{0}', '{-1}','{0}','{0}','{0}','{0}')")
            botInfo.con.commit()
            return 'Вы успешно зарегестрировались! Чтобы открыть меню введите "m"'

def clear(userId):
    botInfo.cur.execute(f"DELETE FROM game WHERE id = {userId}")
    botInfo.con.commit()

def alertMenu(userId):
    bot.send_message(userId, "Меню", reply_markup=menuKeyboard)

def info(userId):
    biz1 = botInfo.cur.execute(f"SELECT biz1 FROM game WHERE id = {userId}").fetchone()[0]
    biz2 = botInfo.cur.execute(f"SELECT biz2 FROM game WHERE id = {userId}").fetchone()[0]
    biz3 = botInfo.cur.execute(f"SELECT biz3 FROM game WHERE id = {userId}").fetchone()[0]
    bizMoney = botInfo.cur.execute(f"SELECT bizMoney FROM game WHERE id = {userId}").fetchone()[0]
    money = botInfo.cur.execute(f"SELECT money FROM game WHERE id = {userId}").fetchone()[0]
    msg = 'Мой профиль: \n' \
          'Баланс - ' + str(money) + ' RUB\n' \
          'Денег в бизнесе - ' + str(bizMoney) + ' RUB \n' \
          'БИЗНЕСЫ ------------ \n' \
          'МАйНИНГ ФЕРМ - ' + str(biz1) + ' Шт.\n' \
          'ШАУРМЕШНЫХ - ' + str(biz2) + ' Шт.\n' \
          'АВТОМОЕК - ' + str(biz3) + ' Шт.\n' \
          'ВСЕ БИЗНЕСЫ ПРИНОСЯТ - ' + str(biz1*2+biz2*4+biz3*8) + ' RUB/Мин.'
    return(msg)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, botInfo.startmessage, reply_markup=keyboard)

@bot.message_handler(commands=['reg'])
def register(message):
    if testUserId(message.chat.id, True):
        bot.send_message(message.chat.id, testUserId(message.chat.id, False), reply_markup=clearKeyboard)
    if testUserId(message.chat.id, True) == False:
        bot.send_message(message.chat.id, testUserId(message.chat.id, False))

menuCom = {'menu', '/menu', 'меню', '/меню', 'м', 'm', '/m', '/м'}

@bot.message_handler(content_types=['text'])
def menu(message):
    if testUserId(message.chat.id, True):
        answer = botInfo.cur.execute(f"SELECT answer FROM game WHERE id = {message.chat.id}").fetchone()[0]
        lvl = botInfo.cur.execute(f"SELECT lvl FROM game WHERE id = {message.chat.id}").fetchone()[0]
        msg = str(message.text).lower()
        if msg in menuCom:
            alertMenu(message.chat.id)
        elif msg == 'баланс':
            bot.send_message(message.chat.id, str(balance(message.chat.id)) + ' RUB', reply_markup=menuKeyboard)
        elif msg == 'заработать':
            bot.send_message(message.chat.id, 'Выберите на чём вы хотите заработать:', reply_markup=earnKeyboard)
        elif msg == 'магазин':
            bot.send_message(message.chat.id, 'Выберите, что хотите купить:', reply_markup=shopKeyboard)
        elif msg == 'мой профиль':
            bot.send_message(message.chat.id, info(message.chat.id), reply_markup=vivodKeyboard)
        elif msg == 'закончить':
            alertMenu(message.chat.id)
            botInfo.cur.execute(f"UPDATE game SET answer = {-1} WHERE id = {message.chat.id}")
            botInfo.cur.execute(f"UPDATE game SET lvl = {0} WHERE id = {message.chat.id}")
        elif str(answer) != str(-1):
            if msg == str(answer) and lvl == 1:
                math(4, message.chat.id)
            elif msg == str(answer) and lvl == 2:
                math(5, message.chat.id)
            elif msg == str(answer) and lvl == 3:
                math(6, message.chat.id)
            else:
                bot.send_message(message.chat.id, 'Это неправильный ответ! Хочешь закончить?',
                                 reply_markup=endKeyboard)
        elif msg == 'mon1000':
            bot.send_message(message.chat.id, '+1000 RUB')
            botInfo.cur.execute(f"UPDATE `game` SET `money` = `money` + {1000} WHERE id={message.chat.id}")
            botInfo.con.commit()
        else:
            bot.send_message(message.chat.id, 'Я не понимаю, что здесь написано, я всего-лишь - бот! =( \n'
                                              'Вы можете открыть меню /menu')

    if testUserId(message.chat.id, True) == False:
        bot.send_message(message.chat.id, 'Вы не зарегестрированы, введите "/reg"')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global lvl
    try:
        if call.message:
            if call.data == 'clearYes' or call.data == 'clearNo':
                if call.data == 'clearYes':
                    bot.send_message(call.message.chat.id, 'Вы успешно удалили свои данные!')
                    clear(call.message.chat.id)
                    register(call.message)
                if call.data == 'clearNo':
                    bot.send_message(call.message.chat.id, 'Вы успешно не сбросили свои данные!')
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Вы уже зарегестрированы, хотите начать сначала?', reply_markup=None)
            if call.data == 'math' or call.data == 'menu':
                if call.data == 'math':
                    bot.send_message(call.message.chat.id, 'Выберите уровень:', reply_markup=mathLevelKeyboard)
                if call.data == 'menu':
                    alertMenu(call.message.chat.id)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Выберите на чём вы хотите заработать:', reply_markup=None)
            if call.data == 'level1' or call.data == 'level2' or call.data == 'level3':
                if call.data == 'level1':
                    math(1, call.message.chat.id)
                    lvl = 1
                if call.data == 'level2':
                    math(2, call.message.chat.id)
                    lvl = 2
                if call.data == 'level3':
                    math(3, call.message.chat.id)
                    lvl = 3
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Выберите уровень:', reply_markup=None)
            if call.data == 'shopMining' or call.data == 'shopShawa' or call.data == 'shopMoika':
                if call.data == 'shopMining':
                    bal = balance(call.message.chat.id)
                    if bal >= 500:
                        botInfo.cur.execute(f"UPDATE `game` SET `money` = `money` - {500} WHERE id={call.message.chat.id}")
                        botInfo.cur.execute(f"UPDATE `game` SET `biz1` = `biz1` + {1} WHERE id={call.message.chat.id}")
                        botInfo.con.commit()
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Вы успешно купили МАЙНИНГ ФЕРМУ', reply_markup=None)
                        alertMenu(call.message.chat.id)
                    else:
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='У вас недостаточно средств!', reply_markup=None)
                        alertMenu(call.message.chat.id)
                if call.data == 'shopShawa':
                    bal = balance(call.message.chat.id)
                    if bal >= 1000:
                        botInfo.cur.execute(
                            f"UPDATE `game` SET `money` = `money` - {1000} WHERE id={call.message.chat.id}")
                        botInfo.cur.execute(
                            f"UPDATE `game` SET `biz2` = `biz2` + {1} WHERE id={call.message.chat.id}")
                        botInfo.con.commit()
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                text='Вы успешно купили ШАУРМЕШНУЮ', reply_markup=None)
                        alertMenu(call.message.chat.id)
                    else:
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                text='У вас недостаточно средств!', reply_markup=None)
                        alertMenu(call.message.chat.id)
                if call.data == 'shopMoika':
                    bal = balance(call.message.chat.id)
                    if bal >= 2500:
                        botInfo.cur.execute(
                            f"UPDATE `game` SET `money` = `money` - {2500} WHERE id={call.message.chat.id}")
                        botInfo.cur.execute(
                            f"UPDATE `game` SET `biz3` = `biz3` + {1} WHERE id={call.message.chat.id}")
                        botInfo.con.commit()
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                text='Вы успешно купили АВТОМОЙКУ', reply_markup=None)
                        alertMenu(call.message.chat.id)
                    else:
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                text='У вас недостаточно средств!', reply_markup=None)
                        alertMenu(call.message.chat.id)
            if call.data == 'vivod':
                bizMon = botInfo.cur.execute(f"SELECT bizMoney FROM game WHERE id = {call.message.chat.id}").fetchone()[0]
                botInfo.cur.execute(f"UPDATE game SET bizMoney = {0}")
                bal = balance(call.message.chat.id)
                botInfo.cur.execute(f"UPDATE game SET money = {bal} + {bizMon}")
                botInfo.con.commit()
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Вывод: УСПЕШНО!', reply_markup=None)
                alertMenu(call.message.chat.id)
    except Exception as e:
        print(repr(e))



bot.polling(none_stop=True)

