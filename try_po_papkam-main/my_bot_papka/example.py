"""Демонстрация работы рассылки сообщений по ближайшему времени"""

import asyncio
from datetime import datetime, timedelta, time

from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, BotCommand, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from database.database import User

bot = Bot(token="token")
dp = Dispatcher()
SEND_TIME = None
router = Router()

@router.message(Command("set_time"))
async def set_time_handler(message: Message):
    """Устанавливаем время рассылки."""
    print(message.text)
    time_split = message.text.replace('/set_time ', '').split(':')
    hour = int(time_split[0])
    minut = int(time_split[1])

    global SEND_TIME
    SEND_TIME = time(hour, minut)
    user = User.get_by_id(1)
    user.time = SEND_TIME
    user.save()

@router.message(Command("start"))
async def start_handler(msg: Message):
    """Обработка команды старт"""
    await bot.set_my_commands([
        BotCommand(command='start',description='Запуск бота'),
        BotCommand(command='help',description='Справка'),
        BotCommand(command='delete',description='Отчислиться'),
        BotCommand(command='set_time',description='Установить время'),
    ])

    markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Привет! 👋')]])
    await msg.answer(text="Привет", reply_markup=markup)


async def get_time_notify():
    """Получить время ближайшей рассылки"""
    now = datetime.now()
    users = User.filter(User.time > now).order_by(User.time.asc())
    if users.count() > 0:
        return (users.first()).time

async def send_admin():
    """Параллельный процесс для рассылки сообщений"""
    global SEND_TIME
    SEND_TIME = await get_time_notify()
    await bot.send_message(320720102, "Бот запущен!")
    while True:
        print(datetime.now().time(), SEND_TIME)
        now_time = datetime.now().time()
        now_time = time(now_time.hour, now_time.minute)
        if SEND_TIME and SEND_TIME == now_time:
            # рассылка уведомлений всем пользователям
            for user in User.filter(time=SEND_TIME):
                await bot.send_message(user.tg_user, 'ping')

            SEND_TIME = await get_time_notify()
            print(SEND_TIME)


        now_time = (datetime.now() + timedelta(minutes=1))
        now_time = datetime(now_time.year, now_time.month, now_time.day,
                            now_time.hour, now_time.minute)
        seconds = (now_time - datetime.now()).seconds + 1
        print(datetime.now().time(), now_time.time(), seconds)
        await asyncio.sleep(seconds)


async def on_startup():
    """Обертка для запуска параллельного процесса"""
    asyncio.create_task(send_admin())

async def main():
    '''Старт бота'''
    dp.startup.register(on_startup)
    dp.include_routers(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())