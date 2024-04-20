import sqlite3 as sq
import pyspapi
import keyboards
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from database.database import add_transaction

rt = Router()

db = sq.connect(r'C:\Users\super\PycharmProjects\SPBOT\database\database.db')
cur = db.cursor()


class Transactions(StatesGroup):
	card = State()
	amount = State()
	comment = State()


@rt.callback_query(F.data == 'trans')
async def transaction_one(call: CallbackQuery, state: FSMContext):
	await state.set_state(Transactions.card)
	await call.message.answer('Введите номер карты получателя')


@rt.message(Transactions.card)
async def transaction_two(message: Message, state: FSMContext):
	await state.update_data(card=message.text)
	await state.set_state(Transactions.amount)
	await message.answer('Введите сумму')


@rt.message(Transactions.amount)
async def transaction_three(message: Message, state: FSMContext):
	await state.update_data(amount=message.text)
	await state.set_state(Transactions.comment)
	await message.answer('Введите комментарий к переводу')


@rt.message(Transactions.comment)
async def transaction_final(message: Message, state: FSMContext):
	await state.update_data(comment=message.text)
	user_id = message.from_user.id
	data = await state.get_data()
	card = data['card']
	amount = data['amount']
	comment = data['comment']
	await add_transaction(user_id, card, amount, comment)
	with sq.connect('database/database.py'):
		table = 'a' + str(user_id)
		cur.execute(f'SELECT id, card, token FROM {table}')
		results = cur.fetchall()
		for row in results:
			print(f"id: {row[0]}, card: {row[1]}, token: {row[2]}")
	try:
		pyspapi.SPAPI(card_id=row[1], token=row[2]).transaction(
			receiver=data["card"], amount=data["amount"], comment=data["comment"])
		await message.answer('Успешно переведено✅', reply_markup=await keyboards.again())
	except Exception as e:
		await message.answer(f'Произошла ошибка: {e}')
	await state.clear()


@rt.callback_query(F.data == 'balance')
async def balance(call: CallbackQuery):
	with sq.connect('database/database.py'):
		user_id = call.from_user.id
		table = 'a' + str(user_id)
		cur.execute(f'SELECT id, card, token FROM {table}')
		results = cur.fetchall()
		for row in results:
			print(f"id: {row[0]}, card: {row[1]}, token: {row[2]}")
	sigma = pyspapi.SPAPI(card_id=row[1], token=row[1]).balance
	await call.message.answer(f'Ваш баланс: {sigma}', reply_markup=await keyboards.again())
