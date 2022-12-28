from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from database.models import File


def history_markup(files: List[File], page: int = 1, pages: int = 1):
    markup = InlineKeyboardMarkup(row_width=3)

    if pages == 1:
        bar = [InlineKeyboardButton(f"{page}/{pages}", callback_data="null")]
    elif page == 1:
        bar = [InlineKeyboardButton(f"{page}/{pages}", callback_data="null"),
        InlineKeyboardButton(">>>", callback_data=f"page:{page + 1}")]
    elif page == pages:
        bar = [InlineKeyboardButton("<<<", callback_data=f"page:{page - 1}"),
        InlineKeyboardButton(f"{page}/{pages}", callback_data="null")]
    else:
        bar = [InlineKeyboardButton("<<<", callback_data=f"page:{page - 1}"),
        InlineKeyboardButton(f"{page}/{pages}", callback_data="null"),
        InlineKeyboardButton(">>>", callback_data=f"page:{page + 1}")]

    for file in files:
        name = 'Фото' if file.file_type == 'photo' else 'Аудио'
        text = f'{name} | {file.filename} | {file.time}'
        call = f'info_{file.id}'
        markup.add(InlineKeyboardButton(text=text, callback_data=call))
    return markup.add(*bar)


def main_menu():
    markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton('Библиотека')]], resize_keyboard=True)
    return markup
