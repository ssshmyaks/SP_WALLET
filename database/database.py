import sqlite3 as sq
from datetime import datetime

db = sq.connect(r'C:\Users\super\PycharmProjects\SPBOT\database\database.db')
cur = db.cursor()

cur.execute('''
	CREATE TABLE IF NOT EXISTS accounts(
	id INTEGER PRIMARY KEY,
	tg INTEGER,
	card TEXT NOT NULL,
	token TEXT NOT NULL
	)''')

cur.execute('''
	CREATE TABLE IF NOT EXISTS transactions(
	id INTEGER PRIMARY KEY,
	tg INTEGER,
	date TEXT NOT NULL,
	card INTEGER,
	amount INTEGER,
	comment TEXT NOT NULL
	)''')


def create_table(user_id: int, card_id: str, token: str):
	table = 'a' + str(user_id)

	cur.execute(f'''
	CREATE TABLE IF NOT EXISTS {table} (
	id INTEGER PRIMARY KEY,
	card TEXT NOT NULL,
	token TEXT NOT NULL
    )''')

	cur.execute(f'INSERT INTO {table} (card, token) VALUES (?, ?)', (card_id, token))
	db.commit()


async def add_user_id_to_db(user_id, card_id: str, token: str):
	with sq.connect('database/database.py'):
		cur.execute("SELECT * FROM accounts WHERE tg = ?", (user_id,))
		cur.execute("SELECT * FROM accounts WHERE card = ?", (card_id,))
		cur.execute("SELECT * FROM accounts WHERE token = ?", (token,))
		user_exists = cur.fetchone() is not None
		if not user_exists:
			cur.execute("INSERT INTO accounts (tg, card, token) VALUES (?, ?, ?)", (user_id, card_id, token))
			db.commit()


async def add_transaction(user_id: int, card: int, amount: str, comment: str):
	with sq.connect('database/database.py'):
		cur.execute("INSERT INTO transactions (tg, date, card, amount, comment) VALUES (?, ?, ?, ?, ?)",
					(user_id, datetime.now(), card, amount, comment))
		db.commit()
