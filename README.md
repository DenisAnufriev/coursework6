# coursework6
---

## Установка и настройка

### 1. Клонирование репозитория
```bash
git clone https://github.com/DenisAnufriev/coursework6.git
cd DenisAnufriev_homework19_2
```

### 2. Установка зависимостей
Проект использует Pip для управления зависимостями.
```bash
pip install -r requirements.txt
```

### 3. Настройка переменных окружения
Создайте файл `.env` в корневой директории проекта и добавьте необходимые переменные окружения, такие как настройки базы данных:
```
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/mydatabase

EMAIL_USE_TLS=True
EMAIL_HOST='smtp.yandex.ru'  # Замените на ваш SMTP-сервер
EMAIL_PORT=465               # Обычно 587 для TLS
EMAIL_HOST_USER="your_mail@yandex.ru"
EMAIL_HOST_PASSWORD="your_password"
```

### 4. Запуск миграций
Чтобы применить миграции, используйте следующую команду:
```bash
python3 manage.py migrate
```


### 6. Запуск проекта
Чтобы запустить сервер, используйте следующую команду:
```bash
python3 manage.py runserver
```
Сервер будет доступен по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000).

### 7. Создание суперпользователя, групп, менеджера и контент менеджера.
admin@test.com
pass = 12345
```bash
python3 manage.py create_super_user
python3 manage.py create_groups
python3 manage.py create_staff
```

---

## Структура проекта
- **mailing/**: приложение для у правления рассылками.
- **users/**: приложение для управления пользователями.
- **templates/**: шаблоны HTML для отображения интерфейса.
- **static/**: статические файлы (CSS, JavaScript, изображения).

---

## Функциональные возможности


---

## Технологии и инструменты
- **Django**: основной фреймворк.
- **PostgreSQL**: база данных.
- **Bootstrap**: для оформления интерфейса.
- **dotenv**: для управления переменными окружения.

---

## Лицензия
Укажите, если проект имеет лицензию.
