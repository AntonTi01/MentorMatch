# MentorMatch Server Container

## Назначение
FastAPI-приложение, которое предоставляет основной REST API MentorMatch. Сервис управляет синхронизацией с Google Sheets, взаимодействует с ботом Telegram и инициирует процессы подбора через сервис matching. Главная точка входа — `server/main.py`, конфигурирующая логирование, соединения с Postgres и прикрепляющая маршруты административного подбора.【F:server/main.py†L1-L120】【F:server/matching_router.py†L1-L40】

## Структура каталога
- `main.py` — инициализация приложения, конфигурация логгера, формирование DSN и HTTP-хендлеры для сервисных операций (импорт тестовых данных, уведомления бота, выгрузка файлов).【F:server/main.py†L24-L154】
- `matching_router.py` — формы и JSON-эндпоинты, которые проксируют запросы на matching-сервис для ручного запуска рекомендаций администраторами.【F:server/matching_router.py†L1-L40】
- `embedding_queue.py` — очередь задач для отложенного обновления эмбеддингов, вызывающая matching API после фиксации транзакций БД.【F:server/embedding_queue.py†L1-L27】
- `media_store.py` — загрузка и сохранение медиафайлов (CV и др.) в локальное хранилище с регистрацией записей в базе.【F:server/media_store.py†L1-L71】
- `clients/` — HTTP-клиенты для вспомогательных сервисов (Google Data и Matching).【F:server/clients/google_data_client.py†L1-L31】【F:server/clients/matching_client.py†L1-L200】
- `services/` — доменные процедуры, например обработка импорта тематик и нормализация ссылок на Telegram.【F:server/services/topic_import.py†L1-L50】

## Ключевые функции
- `_configure_logging()` — читает уровень логирования из окружения и настраивает корневой логгер, обеспечивая единый формат сообщений сервиса.【F:server/main.py†L24-L43】
- `_sync_roles_sheet()` — обращается к Google Data сервису для синхронизации листа ролей и устойчив к ошибкам сети.【F:server/main.py†L45-L66】
- `build_db_dsn()` и `get_conn()` — формируют строку подключения Postgres и создают соединения, поддерживая настройку через `DATABASE_URL` или отдельные переменные окружения.【F:server/main.py†L68-L85】
- `_send_telegram_notification()` — отправляет HTTP-запрос в контейнер бота для доставки уведомлений пользователям с поддержкой inline-кнопок.【F:server/main.py†L101-L158】
- `create_matching_router()` — регистрирует ручные POST-эндпоинты, которые вызывают соответствующие методы matching клиента (`match_topic`, `match_student`, `match_supervisor`, `match_role`).【F:server/matching_router.py†L1-L40】
- `enqueue_refresh()` и `commit_with_refresh()` — собирают запросы на пересчёт эмбеддингов и запускают их через matching API после успешного `commit()` транзакции.【F:server/embedding_queue.py†L11-L27】

## Обмен данными и интеграции
- Зависит от Postgres для хранения основной информации (`build_db_dsn`).【F:server/main.py†L68-L81】
- Использует matching сервис для пересчёта эмбеддингов и выдачи рекомендаций (через `clients/matching_client.py`).【F:server/matching_router.py†L5-L34】【F:server/embedding_queue.py†L11-L27】
- Вызывает Google Data сервис для выгрузки пар и синхронизации листов (`clients/google_data_client.py`).【F:server/main.py†L45-L66】【F:server/clients/google_data_client.py†L1-L31】
- Получает токены и конфигурацию через переменные окружения, подключаемые из `.env` и `docker-compose.yml`.
