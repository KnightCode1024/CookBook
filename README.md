# CookBook
Приложение кулинарной книги на Flask.

## Функционал
- Авторизация
- Добавление рецепта
- Удаление рецепта
- Обнавление рецепта
- Просмотр рецептов

## Технологии
- Flask (основной фреймворк)
- Flask-SQLAlchemy (для работы с БД)
- Flask-Login (для авторизации)
- Flask-WTF (для форм и валидации)
- WTForms (создание форм)
- PostgrSQL (база данных)
- Jinja2 (шаблонизатор)
- HTML/CSS/JavaScript/Bootstrap (Страницы)
- Docker (Контейниризация)

## Запуск 
Создайте файл `.env`. В папке `src/utils` есть скрипт для генирации глючей `generate_secret_key.py`. Запустиек скрипт. Вставте ключ из крнсоли в `.env` в значение переменной `APP_SECRET_KEY`

```env
DB_NAME=cookbook
DB_HOST=database
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=12345678

APP_HOST=0.0.0.0
APP_PORT=8080
APP_DEBUG=1
APP_SECRET_KEY=secret_key
```

Запустите docker контейнеры
```bash
docker compose up --build -d
```

Посмотрите результат на http://127.0.0.1:8080


## Структура
 - `run.py` - запуск приложения
 - `core` - настройки приложений
 - `db` - работа с базой данных
    - `database.py` - основные экземпляры классов для работы с БД 
    - `models` - Модели (Таблицы БД)
    - `repositories` - Репозиторий (Работа с БД)
 - `forms` - обработка и валидация форм
 - `migrations` - миграции БД
 - `routers` - обработчики баршрутов в приложений
 - `services` - сервисный слой работа с БД на уровне приложения
 - `static` - папка для статики с подпапками: css(стили), js(javascript), img(картинки если нужны), uploads(картинки и файлы, но уже для бэкенда)
 - `templates` - папка для html шаблонов 
 - `.env.example` - пример `.env` файла для хранения секретов приложения


## Как делать миграции
```
# Иницализация миграций
flask --app run.py db init

# Создание миграции
flask --app run.py db migrate -m "Initial migration"

# Применение миграций
flask --app run.py db upgrade
```
