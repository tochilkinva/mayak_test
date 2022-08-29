"""
Асинхронный бот Telegram с функцией получения задач и сохранения в базу
Стэк: aiogram, aiosqlite, pandas

Алгоритм работы
1.	Пользователь отправляет файл excel в формате xlsx:
    (название, URL, xpath запрос)
2.	Бот получает файл, сохраняет
3.	Открывает файл библиотекой pandas
4.	Выводит содержимое в ответ пользователю
5.	Сохраняет содержимое в локальную бд sqlite
"""

import logging
import os

import aiosqlite
import pandas as pd
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

bot = Bot(token=TELEGRAM_TOKEN)  # Объект бота
dp = Dispatcher(bot)  # Диспетчер для бота

# Включаем логирование. Пишем логи в файл main.log
logging.basicConfig(
    filename='main.log',
    level=logging.DEBUG,
)


class AIODatabase():
    def __init__(self) -> None:
        pass

    async def create_db(self) -> None:
        """
        Создаем базу данных и таблицы tasks, results
        """
        async with aiosqlite.connect('mayak.db') as db:
            # таблица для задач
            await db.execute('CREATE TABLE IF NOT EXISTS tasks'
                             '(name TEXT UNIQUE, url TEXT, '
                             ' xpath_request TEXT)')
            # таблица для хранения результатов
            await db.execute('CREATE TABLE IF NOT EXISTS results'
                             '(task_id INTEGER, name TEXT, price REAL, '
                             'FOREIGN KEY (task_id) '
                             'REFERENCES tasks (task_id))')
            await db.commit()

    async def save_task_to_db(self, name, url, xpath_request) -> None:
        """
        Сохраняем task в базу
        """
        async with aiosqlite.connect('mayak.db') as db:
            try:
                await db.execute('INSERT OR REPLACE INTO tasks VALUES'
                                 ' (?, ?, ?)',
                                 (name, url, xpath_request))
                await db.commit()
            except Exception as e:
                logging.error(f'Ошибка сохранения в базу: {e}')

    async def load_task_from_db(self) -> dict:
        """
        Загружаем 3 записи task из базы
        :return: dict[name]: (url, xpath_request)
        """
        result = {}
        async with aiosqlite.connect('mayak.db') as db:
            async with db.execute('SELECT * FROM tasks LIMIT 3') as cursor:
                async for row in cursor:
                    result[row[0]] = (row[1], row[2])
        if result == {}:
            raise Exception('Не удалось загрузить записи из базы')

        return result

    async def save_result_to_db(self, name, url, xpath_request) -> None:
        """
        Сохраняем result в базу
        """
        print('save_result_to_db')

    async def load_result_from_db(self) -> dict:
        print('load_result_from_db')


aiodb = AIODatabase()


def get_tasks_from_file(filename: str) -> list:
    """
    Читаем файл и отдаем список задач
    """
    try:
        sheet = pd.read_excel(filename)
    except Exception as e:
        logging.error(f'Ошибка открытия файла: {e}')
        raise Exception(f'Ошибка открытия файла: {e}')
    return sheet.values.tolist()


def tasks_list_to_str(tasks_list: list) -> str:
    """
    Переводим список задач в строку с переносами строк
    """
    tasks = []
    for task in tasks_list:
        tasks.append(' '.join((task[0][0:15], task[1][0:15], task[2][0:15])))
    return '\n'.join(tasks)


async def save_tasks_to_db(tasks_list: list) -> None:
    """
    Сохраняем список задач в базу
    """
    try:
        for task in tasks_list:
            await aiodb.save_task_to_db(task[0], task[1], task[2])
    except Exception as e:
        logging.error(f'Ошибка сохранения task в базу: {e}')
        raise Exception(f'Ошибка сохранения task в базу: {e}')


# Хэндлер на команду /test
@dp.message_handler(commands='test')
async def cmd_test(message: types.Message):
    await message.answer("test")
    # 3. Открывает файл библиотекой pandas
    tasks_list = get_tasks_from_file('data.xlsx')
    # 4. Выводит содержимое в ответ пользователю
    text = tasks_list_to_str(tasks_list)
    await message.answer(text)
    # 5. Сохраняет содержимое в локальную бд sqlite
    await save_tasks_to_db(tasks_list)
    # test = await aiodb.load_task_from_db()
    # print(test)

    await message.answer("test done")
    # 6. парсит данные?


@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def file_handler(message: types.Message):
    """
    Обработчик получения файла и сохранения задачи в базе
    """
    # 2. Бот получает файл excel, сохраняет
    try:
        file_id = message.document.file_id
        file_name = message.document.file_name
        file = await bot.get_file(file_id)
        file_path = file.file_path
    except Exception as e:
        await message.answer('Ошибка при скачивании файла: {e}')
        logging.error(f'Ошибка сохранения в базу: {e}')
        return None

    if (file_name[-4:] != 'xlsx'):
        await message.reply("Неверный формат файла, пришлите в xlsx")
        logging.error(f'Ошибка формата файла: {file_name}')
        return None

    await bot.download_file(file_path, file_name)
    await message.reply("Бот получил файл")

    # 3. Открывает файл библиотекой pandas
    tasks_list = get_tasks_from_file(file_name)
    # 4. Выводит содержимое в ответ пользователю
    text = tasks_list_to_str(tasks_list)
    await message.answer(text)
    # 5. Сохраняет содержимое в локальную бд sqlite
    await save_tasks_to_db(tasks_list)
    await message.answer("Задания сохранены")
    # 6. парсит данные?


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.answer(
        "Бот для парсинга сайтов. "
        "Пришлите файл excel в формате xlsx: название, URL, xpath запрос."
    )


@dp.message_handler(commands="help")
async def cmd_help(message: types.Message):
    await cmd_start(message=message)


async def on_startup_init(dp) -> None:
    """
    Создаем базу, если ее нет
    """
    await aiodb.create_db()


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup_init)
