# CookBook
Приложение кулинарной книги на Flask

## Технологическии 
- Flask (основной фреймворк)
- Flask-SQLAlchemy (для работы с БД)
- Flask-Login (для авторизации)
- Flask-WTF (для форм и валидации)
- WTForms (создание форм)
- PostgrSQL (база данных)
- Jinja2 (шаблонизатор)
- HTML/CSS/JavaScript/Bootstrap (Страницы)
- Docker (Контейниризация)

## Структура
 - `run.py` - запуск приложения
 - `core` - настройки приложений
 - `db` - работа с базой данных
 - `migrations` - миграции БД
 - `routers` - обработчики баршрутов в приложение
 - `templates` - папка для html шаблонов
 - `static` - папка для статики с подпапками: css, js, img
 - `.env.example` - пример `.env` файла для хранения секретов приложения


## Запуск 
```
docker compose up --build -d
```

## Чтобы я не забыл
```
flask --app run.py db init
flask --app run.py db migrate -m "Initial migration"
flask --app run.py db upgrade
```

## ToDo
- [ ] Добавить авторизацию
- [ ] Добавить добавление блюда
- [ ] Просмотр блюд с пагинацией
- [ ] Блюда по категориям
- [ ] Поиск


