# mayak_test
Telegram bot for parsing

### Описание
Telegram-бот, который позволяет обычному пользователю минимальными усилиями добавлять еще сайты для парсинга.  

### Команды
- /start - Появляется при первом старте бота
- /help - Дублирует сообщение команды /start
- Отправка боту файла: название.xlsx - сохраняет файл на диск и загружает задания из него в БД

### Технологии
Python 3.9, aiogram, aiosqlite, pandas

### Запуск проекта

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/tochilkinva/mayak_test.git
cd mayak_test
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
. env/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Создайте файл .env и укажите необходимые данные.
Пример есть в .env_example.
Затем просто запустите код main.py в Python.

### Автор
Валентин
