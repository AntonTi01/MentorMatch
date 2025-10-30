# MentorMatch Bot Container

## Назначение
Контейнер с Telegram-ботом MentorMatch. Скрипт `run_bot.py` загружает переменные окружения, проверяет наличие токена и запускает асинхронное приложение бота, предоставляя также внутренний HTTP API для уведомлений от серверного сервиса.【F:bot/run_bot.py†L1-L45】

## Структура каталога
- `mentormatch.py` — класс `MentorMatchBot`, комбинирующий ядро `BotCore` и миксины обработчиков меню, идентификации, сущностей и подбора.【F:bot/mentormatch.py†L1-L20】
- `core/app.py` — базовый класс `BotCore`, который инициализирует токен, HTTP сервер (`/notify`, `/healthz`), Telegram Application и HTTP-клиент для обращения к REST API бэкенда.【F:bot/core/app.py†L1-L140】
- `dispatcher.py` — регистрирует команды, колбэки и обработчики сообщений Telegram, связывая их с методами бота.【F:bot/dispatcher.py†L1-L80】
- `handlers/` — функциональные миксины:
  - `menu.py` — логика навигации по меню и спискам сущностей.【F:bot/handlers/menu.py†L1-L160】
  - `identity.py` — авторизация пользователей, подтверждение личности и привязка Telegram ID.【F:bot/handlers/identity.py†L1-L69】
  - `entities.py` — просмотр и редактирование студентов, наставников, тем и ролей с использованием HTTP API сервера.【F:bot/handlers/entities.py†L1-L200】
  - `matching.py` — вызов сценариев подбора через REST API и вывод результатов пользователю.【F:bot/handlers/matching.py†L1-L160】
  - `base.py` — общие утилиты и методы отправки сообщений/клавиатур для всех обработчиков.【F:bot/handlers/base.py†L1-L160】
- `services/api_client.py` — асинхронный HTTP клиент на aiohttp для общения с серверным API (GET/POST с обработкой ошибок).【F:bot/services/api_client.py†L1-L44】
- `config.py` — вспомогательные функции загрузки настроек (администраторы, тайм-ауты, параметры HTTP), переиспользуемые в `BotCore`.【F:bot/config.py†L1-L160】

## Ключевые функции
- `BotCore._start_http_server()` / `_handle_notify()` — поднимают внутренний веб-сервер, принимающий POST/GET уведомления от сервисов и пересылающий их в Telegram чат с учётом inline-кнопок и флагов предпросмотра.【F:bot/core/app.py†L60-L140】
- `dispatcher.setup()` — подключает все команды, callback handlers и обработчики ошибок к экземпляру Telegram Application, чтобы миксины могли реагировать на действия пользователя.【F:bot/dispatcher.py†L1-L80】
- Методы из миксинов (например, `MatchingHandlers.cb_match_topics_for_me`, `EntityHandlers.cb_edit_topic_start`) вызывают REST API и формируют ответы, обеспечивая полный цикл взаимодействия без использования веб-интерфейса.【F:bot/handlers/matching.py†L1-L160】【F:bot/handlers/entities.py†L1-L200】

## Интеграции
- Использует переменные окружения `TELEGRAM_BOT_TOKEN`, `SERVER_URL`, `BOT_HTTP_HOST`, `BOT_HTTP_PORT`, задаваемые в `docker-compose.yml`, для настройки доступа к Telegram и REST API серверного контейнера.【F:docker-compose.yml†L118-L143】
- Принимает уведомления от серверного сервиса через HTTP POST `/notify`, что позволяет инициировать сообщения пользователям из бэкенда.【F:bot/core/app.py†L70-L140】
- Делит каталог `templates/` в режиме `read-only` для генерации HTML/текстовых сообщений, рендеримых ботом при необходимости (через handlers).【F:docker-compose.yml†L118-L143】
