# Система управления курьерами

Консольное и веб-приложение для управления курьерами и заказами службы доставки.

## Назначение

Приложение автоматизирует работу службы доставки: позволяет вести учёт курьеров, создавать заказы, назначать их курьерам, отслеживать статусы и формировать маршруты.

## Предметная область

Курьерская доставка — процесс перемещения товаров от отправителя к получателю. Основные понятия: курьер, заказ, пользователь (диспетчер), маршрут.

## Основные сущности

### Courier — курьер

Атрибуты: id, name, phone, transport, zone, status, orders_done.

Методы: is_available(), can_take_order(), complete_order(), set_status(), __str__().

### User — пользователь (диспетчер)

Атрибуты: id, name, email, role.

Методы: from_data(), __str__().

### Order — заказ

Атрибуты: id, number, address, recipient, phone, weight, cost, date, courier, user, route, status.

Методы: assign_to(), assign_to_route(), cancel(), complete(), is_new(), is_in_route(), __str__().

### Route — маршрут

Атрибуты: id, courier, date, orders, is_completed.

Методы: add_order(), remove_order(), get_total_weight(), get_total_cost(), get_orders_count(), complete(), __str__().

## Структура проекта

courier-management-system/

- manage.py — управление Django-проектом
- main.py — консольная версия
- storage.py — JSON-загрузка и сохранение
- utils.py — безопасный ввод
- requirements.txt — зависимости
- .flake8 — настройки линтера
- .gitignore — исключения Git
- README.md — документация

- couriermanager/ — пакет настроек Django
- homepage/ — Django-приложение: главная страница
- courier/ — Django-приложение: курьеры
- order/ — Django-приложение: заказы
- models/ — классы предметной области (ПР3)
- data/ — JSON-файлы данных
- tests/ — тесты pytest

## Веб-интерфейс (ПР5)

Django-проект: couriermanager, версия Django 5.2.

Приложения: homepage, courier, order.

Локализация: ru-RU, Europe/Moscow.

### Страницы

- / — главная (homepage.views.index)
- /couriers/ — список курьеров (courier.views.couriers_list)
- /couriers/<int:courier_id>/ — карточка курьера (courier.views.courier_detail)
- /orders/ — список заказов (order.views.orders_list)
- /orders/<int:order_id>/ — карточка заказа (order.views.order_detail)

При несуществующем идентификаторе возвращается страница с кодом 404.

Общий обработчик 404: handler404 = "homepage.views.page_not_found".

### Назначение модулей Django

- homepage — главная страница и функция page() — единый HTML-каркас с Bootstrap
- courier — страницы курьеров
- order — страницы заказов
- couriermanager/urls.py — корневая маршрутизация через include()

### Оформление

Bootstrap 5.3 через CDN. Используются: navbar, container, card, badge, btn, list-group.

## Консольная версия (ПР3)

Сохранена и работает.

Запуск: python main.py

Меню включает: добавление курьеров, пользователей, заказов; создание маршрутов; назначение заказов; отмену; поиск; сортировку.

## Хранение данных

Данные хранятся в JSON-файлах в каталоге data/:

- couriers.json
- users.json
- orders.json
- routes.json

При загрузке JSON преобразуется в объекты Courier, User, Order, Route. При сохранении — обратно в JSON. Связи между объектами в JSON хранятся через идентификаторы: courier_id, user_id, route_id.

## Установка и запуск

Создать окружение:

python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Django-версия:

python manage.py migrate
python manage.py runserver

Открыть в браузере: http://127.0.0.1:8000/

Консольная версия:

python main.py

## Тестирование

pytest -v

Все тесты должны завершиться успешно.

## Проверка качества кода

flake8 . --extend-exclude=venv

При отсутствии замечаний команда ничего не выводит.

## Зависимости

- Django==5.2.* — веб-фреймворк
- pytest>=8.0 — тестирование
- flake8>=7.0 — проверка качества кода

## Git

Состояние репозитория:

git status
git log --oneline

## Текущее состояние и план развития

Реализовано:

- ПР1: основы Python, рабочее окружение, Git
- ПР2: коллекции, функции, модули, JSON, тесты, flake8
- ПР3: ООП — классы Courier, User, Order, Route
- ПР5: Django-проект, три приложения, маршрутизация, view-функции, веб-страницы, Bootstrap, обработка 404

Планируется:

- ПР6: Django-шаблоны, контекст, наследование шаблонов, статические файлы
- ПР7: Django ORM, база данных, модели
- ПР10: Django Forms
- ПР11: аутентификация и авторизация
- ПР13–15: тестирование и Docker