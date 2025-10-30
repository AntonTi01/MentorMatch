# MentorMatch Admin Container

## Назначение
Веб-интерфейс администраторов MentorMatch на FastAPI с серверным рендерингом шаблонов. Позволяет просматривать пользователей и темы, инициировать импорт из Google Sheets и запускать процессы подбора напрямую из браузера. Главный модуль `admin/main.py` создаёт приложение, подключает шаблоны Jinja2 и регистрирует маршруты административных страниц.【F:admin/main.py†L1-L20】

## Структура каталога
- `main.py` — точка входа FastAPI, загружает переменные окружения, создаёт экземпляр приложения и подключает роутер административных страниц.【F:admin/main.py†L1-L20】
- `router.py` — собирает `APIRouter`, передавая контекст подключения к базе и шаблонов во все модули представлений.【F:admin/router.py†L1-L16】
- `context.py` — dataclass с зависимостями (фабрика соединений и Jinja2 шаблоны), который используется в представлениях для доступа к БД и шаблонам.【F:admin/context.py†L1-L9】
- `views/` — набор модулей FastAPI route handlers:
  - `dashboard.py` выводит главную панель с вкладками студентов, наставников и тем, объединяя данные и контекст для шаблонов.【F:admin/views/dashboard.py†L1-L120】
  - `topics.py` управляет карточками тем, включая редактирование и подтверждение наставников/студентов.【F:admin/views/topics.py†L1-L200】
  - `users.py` обрабатывает просмотр профилей пользователей и действия подтверждения ролей.【F:admin/views/users.py†L1-L200】
  - `imports.py` предоставляет формы и POST-эндпоинты для запуска импорта данных из Google Sheets.【F:admin/views/imports.py†L1-L120】
  - `matching.py` проксирует действия подбора в matching сервис через HTTP-клиенты и возвращает статусы пользователю.【F:admin/views/matching.py†L1-L32】
  - `requests.py` управляет согласованием заявок и ручными запросами пользователей.【F:admin/views/requests.py†L1-L200】
- `clients/` — HTTP-клиенты для сервисов matching и google_data, используемые в представлениях и очереди эмбеддингов.【F:admin/clients/matching_client.py†L1-L80】【F:admin/clients/google_data_client.py†L1-L31】
- `embedding_queue.py`, `media_store.py`, `utils.py`, `utils_common.py` — общие утилиты с серверным контейнером для обработки медиа, очередей эмбеддингов и парсинга параметров.【F:admin/embedding_queue.py†L1-L27】【F:admin/media_store.py†L1-L71】【F:admin/utils_common.py†L1-L120】

## Ключевые функции и обработчики
- `create_admin_router()` — создаёт контекст и регистрирует модули представлений, обеспечивая единый интерфейс для всех административных страниц.【F:admin/router.py†L5-L15】
- В `dashboard.register()` реализована пагинация по студентам, наставникам и темам, а также запуск фоновой синхронизации и подтверждений через очередь эмбеддингов.【F:admin/views/dashboard.py†L1-L200】
- `matching.register()` определяет POST-эндпоинты `/do-match-*`, которые вызывают HTTP-клиентов matching сервиса и возвращают статус через редирект с сообщением.【F:admin/views/matching.py†L1-L32】
- `imports.register()` вызывает Google Data сервис для импорта студентов и наставников из таблиц, обрабатывая выбор сервисного аккаунта и ошибок доступа.【F:admin/views/imports.py†L1-L120】
- Общие утилиты `enqueue_refresh()`/`commit_with_refresh()` синхронизированы с matching сервисом, обеспечивая пересчёт эмбеддингов после изменений в админке.【F:admin/embedding_queue.py†L11-L27】

## Интеграции
- Подключается к Postgres через `db.get_conn()` с использованием настроек из окружения `.env`/`docker-compose` для чтения и изменения данных платформы.【F:admin/db.py†L1-L120】
- Обменивается с matching сервисом и Google Data через HTTP-клиентов в `clients/`, используя адреса контейнеров из переменных окружения.【F:admin/clients/matching_client.py†L1-L80】【F:admin/clients/google_data_client.py†L1-L31】
- Разделяет с сервером общий том `media_data` для хранения загруженных файлов и повторного использования утилит работы с медиа.【F:docker-compose.yml†L24-L51】
