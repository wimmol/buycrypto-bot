import asyncio
import logging

from app.bot.handlers import router
from app.bot.bot import bot
from app.bot.dispatcher import dp

dp.include_router(router)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(dp.start_polling(bot))
    except KeyboardInterrupt:
        print('Exit')

