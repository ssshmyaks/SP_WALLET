from aiogram import Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

rt = Router()


async def start_keyboard():
    return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Привязать карту",
                        callback_data="connect"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Перевод",
                        callback_data="trans"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Как получить id и token",
                        callback_data="help"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Проверить на наличие проходки",
                        callback_data="check"
                    )
                ]
            ]
        )


async def again():
    return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Перевести еще раз",
                        callback_data="trans"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Баланс (не работает)",
                        callback_data="balance"
                    )
                ]
            ]
        )
