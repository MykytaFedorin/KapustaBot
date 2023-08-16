from loader import dp
from aiogram.types import Message


@dp.message_handler(commands = ['start'])
async def show_products(message: Message):
    await message.answer('hell')
