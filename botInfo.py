import sqlite3 as sql

token = "1626441599:AAEEwpCI-3LTtZuesgcRCY8y-ltvrt1l5h4"

con = sql.connect('game.db', check_same_thread=False)
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'game' ('id' INTEGER, 'money' INTEGER, 'lvl' INTEGER, 'answer' INTEGER,"
                "'bizMoney' INTEGER,'biz1' INTEGER, 'biz2' INTEGER, 'biz3' INTEGER)")
    con.commit()

startmessage = 'Привет! Я - игровой бот! Чтобы зарегестрироваться, напиши "/reg", если ты захочешь начать сначала,' \
               'то можешь снова написать "/reg"'