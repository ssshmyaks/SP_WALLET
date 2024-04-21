import keyboards
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from database.database import add_user_id_to_db, create_table

rt = Router()


class Card(StatesGroup):
	id = State()
	token = State()


@rt.message(Command('start'))
async def start(message: Message):
	await message.answer(f'Привет {message.from_user.first_name}, я бот, который добавляет возможности сайта сп в телеграм', reply_markup=await keyboards.start_keyboard())


@rt.callback_query(F.data == 'help')
async def connect(call: CallbackQuery):
	await call.message.answer('Получить ID и токен можно на странице "Кошелёк", в секции "Поделиться картой"')


@rt.callback_query(F.data == 'connect')
async def card1(call: CallbackQuery, state: FSMContext):
	await state.set_state(Card.id)
	await call.message.answer('Отправьте ID карты')


@rt.message(Card.id)
async def card2(message: Message, state: FSMContext):
	await state.update_data(id=message.text)
	await state.set_state(Card.token)
	await message.answer('Отправьте токен карты')


@rt.message(Card.token)
async def card3(message: Message, state: FSMContext):
	await state.update_data(token=message.text)
	user_id = message.from_user.id
	data = await state.get_data()
	card_id = data["id"]
	token = data["token"]
	await add_user_id_to_db(user_id, card_id, token)
	create_table(user_id, card_id, token)
	await message.answer('Карта успешно привязана!')
	await state.clear()
