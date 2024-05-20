""" импорт asyncio """
from datetime import datetime, time, timedelta
import asyncio
from aiogram import Bot, Dispatcher
from handlers import include_router
from config import TOKEN
from database.database import FileClass
from handlers.singleton import GlobalVars

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def get_list_users():
    lst = []
    counter = 1
    us = FileClass.get_or_none(id=counter)
    while us != None:
        lst.append(us)
        counter += 1
        us = FileClass.get_or_none(id=counter)
    return lst

async def get_time_notify():
    """Получить время ближайшей рассылки"""
    minute_now, hours_now = datetime.now().minute, datetime.now().hour
    #print(hours_now, minute_now)
    now = time(hour=hours_now, minute=minute_now)
    #users = sorted(await get_list_users(), key=lambda x: x.time)
    users_sort = await get_list_users()
    print(users_sort)
    len_users = len(users_sort)
    users = list(filter(lambda x: x.time > now, users_sort))
    print(users)
    if len(users) > 0:
        return users_sort, len_users, users[0].time, users[0].user_id_tg
    else:
        if len(users_sort) > 0:
            return users_sort, len_users, users_sort[0].time, users_sort[0].user_id_tg

async def send_admin():
    """Параллельный процесс для рассылки сообщений"""
    lst_users, len_users, send_time, send_id = await get_time_notify()
    await bot.send_message(740460453, "Бот запущен!")
    while True:
        print(datetime.now().time(), send_time)
        now_time = datetime.now().time()
        print(now_time)
        await bot.send_message(740460453, "я в цикле")
        now_time = time(now_time.hour, now_time.minute)
        if send_time and send_time == now_time:
            # рассылка уведомлений всем пользователям
            for user in filter(lambda x: x.time==send_time, lst_users):
                await bot.send_message(user.user_id_tg, 'ping')

            send_time = await get_time_notify()
            print(send_time)

        """ if len(await get_list_users()) != len_users:
            lst_users, len_users, send_time, send_id = await get_time_notify() """
        
        if GlobalVars.flag_change_len:
            GlobalVars.flag_change_len = False
            lst_users, len_users, send_time, send_id = await get_time_notify()
        print(GlobalVars.flag_change_len)

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
    """ подключение роутеров и запуск бота """
    dp.startup.register(on_startup)
    include_router(dp)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
