from datetime import datetime, time, timedelta
from aiogram import F, Router
from aiogram.types import Message,CallbackQuery
#from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
#import asyncio

#import my_bot_papka.keyboards.anketa as kbss
import states.anketa as state_user

from database.database import FileClass
#import my_bot_papka.database.take_info as take_info

from handlers.singleton import GlobalVars

router_start = Router()

start_txt = 'Привет!\nЭто бот подарит тебе настроение, рассказав о сегодяншнем празднике.'

@router_start.callback_query(F.data == 'set_time')
async def set_settings_rassilka(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Отправьте время в формате ЧЧ:ММ')
    await state.set_state(state_user.User.time)

@router_start.message(state_user.User.time)
async def set_time(message: Message, state: FSMContext):
    if message.content_type != 'text':
        await message.answer('Вы должны ввести сообщение. Попробуйте еще раз')
        return
    if ':' not in message.text:
        await message.answer('Введенное время должно содержать двоеточие (:)')
        return
    hours, minute = str(message.text).split(':')
    if not hours.isdigit() or not minute.isdigit():
        await message.answer('Час и минута - целые числа')
        return
    if len(hours) != 2 or len(minute) != 2:
        await message.answer('Час и минута должны состоять из двух цифр')
        return
    elif not 0 <= int(hours) <= 23:
        await message.answer('Неправильно указан час')
        return
    elif not 0 <= int(minute) <= 59:
        await message.answer('Неправильно указана минута')
        return
    #FileClass.get_or_none(user_id_tg=message.from_user.id)
    if FileClass.get_or_none(user_id_tg=message.from_user.id) is None:
        FileClass.create(user_id_tg=message.from_user.id, time=time(hour=int(hours), minute=int(minute)))
    else:
        user = FileClass.get(user_id_tg=message.from_user.id)
        user.time =  time(hour=int(hours), minute=int(minute))
        user.save()
    await message.answer(f'Установлено время рассылки на {hours}:{minute}')
    GlobalVars.flag_change_len = True
    await state.clear()
