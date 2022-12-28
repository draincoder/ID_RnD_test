import asyncio
import logging

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message, ContentType, InputFile, ParseMode

import keyboards.inline as inl
from database.crud import Database
from services.converter import format_audio, find_face

logger = logging.getLogger(__name__)


async def user_start(message: Message, db: Database, state: FSMContext):
    text = 'Привет! Это тестовое задание для отклика на вакансию ' \
           '<code>Data Collection Specialist (Junior Python Developer)</code>' \
           '\n\nСоздатель: @treaditup\nСсылка на hh: ' \
           '<a href="https://spb.hh.ru/resume/a4dd9cdcff0b8606440039ed1f4334657a4d52">резюме</a>\n\n' \
           '<b>1)</b> Чтобы конвертировать голосовое сообщение в формат .wav с частотой дискретизации 16кГц и ' \
           'добавить в библиотеку - просто пришлите голосовое сообщение\n' \
           '<b>2)</b> Чтобы добавить в библиотеку фото, на котором изображено лицо - просто пришлите эту фотографию'

    await message.answer(text, reply_markup=inl.main_menu(), parse_mode=ParseMode.HTML)


async def get_audio(message: Message, db: Database, state: FSMContext):
    try:
        file = await message.voice.get_file()
        filename = f"{message.message_id}_{message.from_user.id}.ogg"
        await file.download(destination_file=f'audios/{filename}')
        await message.answer('Подождите, идет обработка...')
        loop = asyncio.get_running_loop()
        file_out = await loop.run_in_executor(None, format_audio, filename)
        msg = await message.answer_audio(InputFile(f'audios/{file_out}'), caption='Файл успешно добавлен!')
        await db.add_file(message.from_user.id, 'audio', '.wav', msg.audio.file_id, file_out.replace('.wav', ''))
    except Exception as e:
        logger.error(e)


async def get_photo(message: Message, db: Database, state: FSMContext):
    try:
        file = await message.photo[-1].get_file()
        filename = f"{message.message_id}_{message.from_user.id}.png"
        await file.download(destination_file=f'photos/{filename}')
        await message.answer('Подождите, идет обработка...')
        loop = asyncio.get_running_loop()
        file_out = await loop.run_in_executor(None, find_face, filename)
        if not file_out:
            return await message.answer('Лица не обнаружены, файл не добавлен.')
        await db.add_file(message.from_user.id, 'photo', '.png', file.file_id, file_out.replace('.png', ''))
        await message.answer_photo(InputFile(f'photos/{file_out}'), caption='Файл успешно добавлен!')
    except Exception as e:
        logger.error(e)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, CommandStart(), state="*")
    dp.register_message_handler(get_audio, state="*", content_types=ContentType.VOICE)
    dp.register_message_handler(get_photo, state="*", content_types=ContentType.PHOTO)
