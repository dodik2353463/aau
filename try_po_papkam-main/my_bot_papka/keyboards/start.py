from aiogram.types import  InlineKeyboardMarkup, InlineKeyboardButton


kb_start = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Задать время рассылки',
            callback_data='set_time')],
    [
        InlineKeyboardButton(
        text='Узнать время рассылки',
        callback_data='take_time')],
    [
        InlineKeyboardButton(
        text='Отказаться от рассылки',
        callback_data='delete_time')
    ]])
