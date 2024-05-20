"""Файл с состояниями, используемыми при анкете (установке времени)"""
from aiogram.fsm.state import State, StatesGroup


class User(StatesGroup):
    """Класс состояний для установки вреимени рассылки"""
    time = State()
