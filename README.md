# Street Shop

Интернет-магазин мужской брендовой одежды с полным циклом покупки. 
Реализован на Django с адаптивным интерфейсом на Bootstrap 5.

## Возможности

- Каталог товаров с фильтрацией по названию бренда
- Регистрация и аутентификация пользователей
- Личный кабинет с историей заказов и редактированием профиля
- Корзина с контролем остатков на складе
- Тестовая оплата (карта 4242 4242 4242 4242)
- Адаптивный дизайн (мобильные устройства)
- Админ-панель для управления товарами и заказами

## Технологии

- Python 3.13
- Django 5.2
- SQLite 
- HTML5, CSS3, Bootstrap 5
- Pillow (обработка изображений)

## Установка и запуск

```bash
# 1. Клонировать репозиторий
git clone https://github.com/RomanMetan/street-shop.git
cd kontakt_market

# 2. Создать виртуальное окружение
python -m venv venv

# 3. Активировать
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Установить зависимости
pip install -r requirements.txt

# 5. Применить миграции
python manage.py migrate

# 6. Запустить сервер
python manage.py runserver
