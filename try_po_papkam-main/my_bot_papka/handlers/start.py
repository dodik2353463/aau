from aiogram import Router, F 
from aiogram.filters import Command
from aiogram.types import BotCommand, Message, CallbackQuery
import keyboards.start as kb_start


router = Router()
start_message = 'Привет!\nЭто бот подарит тебе настроение, рассказав о сегодяншнем празднике.'

@router.message(Command("start"))
async def start_handler(msg: Message):
    """ Обработка команды /start """
    # pylint:disable=C0415
    from main import bot
    await bot.set_my_commands([
        BotCommand(command = 'start', description='Запуск бота'),
        BotCommand(command = 'help', description='Справка'),
    ])

    await msg.answer(text=start_message, reply_markup=kb_start.kb_start)
