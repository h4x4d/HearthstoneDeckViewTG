from gevent.monkey import patch_all
from PIL.Image import Image

patch_all(thread=False, select=False)

import asyncio
import os

from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

from config import TOKEN
from image_creator import create_picture

bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher()
router = Router()


@router.message(Command('start'))
async def process_start_command(message: types.message):

    await message.answer(f'Hi {message.chat.first_name}!\n'
                         f'This bot can help you to represent '
                         f'Hearthstone deck codes via beautiful '
                         f'pictures\n\n'
                         f'This bot can be added to chat with admin rights '
                         f'to post pictures when '
                         f'someone in chat sends it\n\n'
                         f'Developer: @h4x4d\n'
                         f'Github: https://github.com/h4x4d/HearthstoneDeckViewTG\n'
                         f'Donate links: https://vk.com/topic-212733185_49370263')


@router.message(F.text)
async def find_code_in_message(message: types.message):
    text = message.text

    for word in text.split():
        if word.startswith('AA'):
            image: Image = await create_picture(word)

            if not image:
                return

            image.save(f"image.png", format="PNG")
            await message.answer_photo(FSInputFile("image.png"))
            os.remove('image.png')


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
