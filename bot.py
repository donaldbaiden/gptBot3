import asyncio
import os
import tempfile
from aiogram import Bot, Dispatcher, types, filters, F

from amplt import log_user_action
from config import settings
import gpt

bot = Bot(token=settings.telegram_token)
dp = Dispatcher()


@dp.message(filters.CommandStart())
async def start(message: types.message):
    user_id = str(message.from_user.id)
    await log_user_action(user_id, 'started_bot')
    await message.reply("Привет, отправь мне изображение!")


@dp.message(F.photo)
async def photo_handler(message: types.message):
    user_id = str(message.from_user.id)
    await log_user_action(user_id, 'sent_photo')

    photo = message.photo[-1].file_id
    fd, photo_file_path = tempfile.mkstemp(suffix='.png')
    os.close(fd)
    await bot.download(photo, destination=photo_file_path)

    response = await gpt.get_emote(photo_file_path)
    await message.reply(response)

    os.remove(photo_file_path)


async def main():
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
