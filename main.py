#Bot by ssshmyaks
import asyncio
import logging
import config
import transactions
import start
from aiogram import Bot, Dispatcher


bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()


logging.basicConfig(format='[+] %(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

dp.include_routers(start.rt, transactions.rt)


async def main():
    b = Bot(token=config.BOT_TOKEN)
    await dp.start_polling(b, skip_updates=True, on_startup=None)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO)
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
