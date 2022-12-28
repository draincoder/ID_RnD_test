import logging

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, CallbackQuery

import keyboards.inline as inl
from database.crud import Database
from database.models import File
from filters import PrivateChat

logger = logging.getLogger(__name__)


async def get_history(message: Message, db: Database, state: FSMContext):
    try:
        files = await db.get_files(message.from_user.id)
        if not files:
            return await message.answer('Библиотека пуста.')
        page = 1
        items = len(files)
        files.sort(key=lambda x: x.id, reverse=True)
        files = files[(page - 1) * 5:page * 5]
        pages = items // 5
        if items % 5 != 0:
            pages += 1
        await message.answer('Файлы', reply_markup=inl.history_markup(files, pages=pages, page=page))
    except Exception as e:
        logger.error(e)


async def change_page(call: CallbackQuery, db: Database, state: FSMContext):
    try:
        await call.answer()
        page = int(call.data.replace('page:', ''))
        files = await db.get_files(call.from_user.id)
        files.sort(key=lambda x: x.id, reverse=True)
        items = len(files)
        files = files[(page - 1) * 5:page * 5]
        pages = items // 5
        if items % 5 != 0:
            pages += 1
        await call.message.edit_text('Файлы', reply_markup=inl.history_markup(files, pages=pages, page=page))
    except Exception as e:
        logger.error(e)


async def get_info(call: CallbackQuery, db: Database, state: FSMContext):
    try:
        await call.answer()
        file_id = int(call.data.replace('info_', ''))
        file: File = await db.get_file(file_id)
        caption = f'ID: {file.filename}\n' \
                  f'UserID: {file.user_id}\n' \
                  f'Тип: {"Фото" if file.file_type == "photo" else "Аудио"}\n' \
                  f'Дата добавления: {file.time}'
        if file.file_type == 'audio':
            await call.message.answer_audio(file.file_id, caption=caption)
        else:
            await call.message.answer_photo(file.file_id, caption=caption)
    except Exception as e:
        logger.error(e)


def register_history(dp: Dispatcher):
    dp.register_message_handler(get_history, Command('library'), PrivateChat(), state="*")
    dp.register_message_handler(get_history, Text('Библиотека'), PrivateChat(), state="*")
    dp.register_callback_query_handler(change_page, text_startswith='page', state="*")
    dp.register_callback_query_handler(get_info, text_startswith='info', state="*")
