# Prompt Log — Лабораторная работа №12

**Студент:** Кучеров Олег  
**Вариант:** 10 — Банковское приложение  
Журнал всех промптов и ответов ИИ в процессе выполнения работы.

---

## Промпт 0.1 — Инициализация структуры проекта

**Дата:** 2026-05-15

**Промпт:**
```
Инициализируй git-репозиторий для проекта «Банковское приложение» и создай
файловую структуру. Выполни: git init, git remote add origin <url>.
Создай структуру: app/{api/v1, core, models, repositories, schemas, services},
alembic/versions, tests, docs, scripts, sql, .github/workflows.
Создай README.md с данными студента и PROMPT_LOG.md.
Коммит: «chore: initialize git repository and project structure».
```

**Результат:** Инициализирован git-репозиторий. Создана полная файловая структура проекта. Созданы заглушки для всех модулей. Созданы README.md и PROMPT_LOG.md.

---

## Промпт 0.2 — Конфигурация окружения

**Дата:** 2026-05-15

**Промпт:**
```
Создай .gitignore для Python/FastAPI проекта: исключи __pycache__/, *.pyc, .env,
.venv/, .pytest_cache/, htmlcov/, .coverage, coverage.xml, *.sqlite3, alembic/versions/*.py.
Создай .env.example с переменными DATABASE_URL, SECRET_KEY, ALGORITHM,
ACCESS_TOKEN_EXPIRE_MINUTES, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB.
Коммит: «chore: add .gitignore and .env.example».
```

**Результат:** Создан `.gitignore` с 14 правилами. Создан `.env.example` с 8 переменными окружения. Обновлён PROMPT_LOG.md.

---

## Промпт 0.3 — pyproject.toml

**Дата:** 2026-05-15

**Промпт:**
```
Создай pyproject.toml для банковского приложения. build-system = hatchling.
Зависимости: fastapi, uvicorn, sqlalchemy[asyncio], asyncpg, aiosqlite, alembic,
python-jose[cryptography], passlib[bcrypt], bcrypt<5.0.0, pydantic-settings,
pydantic[email], python-multipart, httpx.
Dev-зависимости: pytest, pytest-asyncio, pytest-cov, faker, ruff, mypy, bandit.
Настройки: asyncio_mode=auto, pythonpath=["."], coverage.omit bad_commission.py.
Коммит: «chore: add pyproject.toml with all dependencies».
```

**Результат:** Создан `pyproject.toml` с hatchling backend, 14 production и 7 dev зависимостями. Настроены инструменты: pytest (asyncio_mode=auto), ruff (line-length=100), mypy (python_version=3.12), coverage.

---

## Промпт 1.1 — SQLAlchemy ORM-модели

**Дата:** 2026-05-15

**Промпт:**
```
Ты — senior Python разработчик. Реализуй SQLAlchemy 2.0 async ORM-модели
для банковского приложения.

app/models/base.py: Base = DeclarativeBase(), TimestampMixin с created_at/updated_at.

app/models/user.py — модель User: id, username (unique, index), email (unique, index),
hashed_password, full_name, phone (optional), is_active (bool), role (Enum client/admin).
Relationship → accounts.

app/models/account.py — Account: id, owner_id (FK→users), account_number (unique, index),
account_type (Enum checking/savings/credit), balance (Numeric 15,2), currency (String 3),
is_active (bool). Relationships → user, cards, transactions.

app/models/card.py — Card: id, account_id (FK→accounts), card_number (unique, index),
cardholder_name, expiry_date (Date), card_type (Enum debit/credit), is_blocked (bool).
Relationship → account.

app/models/transaction.py — Transaction: id, account_id (FK→accounts),
transaction_type (Enum debit/credit/transfer_in/transfer_out/payment, index),
amount (Numeric 15,2), balance_after (Numeric 15,2), description, reference_id,
status (Enum completed/failed/pending). Relationship → account.

Все модели с Mapped[], docstring, lazy="selectin". Импорт через models/__init__.py.
Коммит: «feat(models): add SQLAlchemy ORM models for banking entities».
```

**Результат:** Реализованы 4 ORM-модели + base.py. User (таблица users), Account (accounts), Card (cards), Transaction (transactions). Настроены все FK-связи и back_populates. Все модели экспортируются через `app/models/__init__.py`. Импорт проверен — ошибок нет.

---

## Промпт 1.2 — Core-слой

**Дата:** 2026-05-15

**Промпт:**
```
Ты — senior Python разработчик. Реализуй core-слой.

app/core/config.py: Settings(BaseSettings) с DATABASE_URL, SECRET_KEY, ALGORITHM,
ACCESS_TOKEN_EXPIRE_MINUTES, APP_NAME, APP_VERSION, DEBUG; синглтон settings.

app/core/security.py: PWD_CONTEXT=CryptContext(bcrypt), hash_password,
verify_password, create_access_token (с exp-клеймом), decode_token (None при ошибке).

app/core/dependencies.py: create_async_engine + async_sessionmaker; get_db() —
AsyncGenerator с yield; oauth2_scheme=OAuth2PasswordBearer; get_current_user() —
декодирует токен, ищет по username, 401; get_current_active_user() — 403 если деактивирован;
require_role(*roles) — фабрика dependency, 403 если роль не подходит.

app/main.py: FastAPI с lifespan (create_all), CORSMiddleware, 6 роутеров с prefix="/api/v1",
GET /health.
Коммит: «feat(core): add config, JWT security, and dependency injection».
```

**Результат:** Реализованы config.py (Settings + синглтон), security.py (bcrypt + JWT encode/decode), dependencies.py (get_db, get_current_user, get_current_active_user, require_role), main.py (FastAPI + lifespan + CORS + 6 роутеров + /health). Добавлено ограничение `bcrypt<5.0.0` для совместимости с passlib.

---

## Промпт 1.3 — Repository-слой

**Дата:** 2026-05-15

**Промпт:**
```
Ты — senior Python разработчик. Реализуй Repository-слой.

base_repository.py — Generic[ModelType]: get, get_all (skip/limit), create, update, delete.

user_repository.py — UserRepository: get_by_email, get_by_username, get_active_clients.

account_repository.py — AccountRepository: get_by_account_number, get_by_owner (owner_id,
только активные), get_active.

card_repository.py — CardRepository: get_by_card_number, get_by_account,
get_active_by_account (is_blocked=False).

transaction_repository.py — TransactionRepository: get_by_account (paginated, order by
created_at desc), get_by_type (account_id + transaction_type).

Все методы async, type hints. Синглтоны для каждого репозитория.
Коммит: «feat(repositories): add data access layer with generic base repository».
```

**Результат:** Реализованы 5 файлов репозиториев. BaseRepository (5 методов CRUD), UserRepository (3 метода), AccountRepository (3 метода), CardRepository (3 метода), TransactionRepository (2 метода). Обновлён `repositories/__init__.py`. Все синглтоны (`user_repository`, `account_repository`, `card_repository`, `transaction_repository`) проверены.

---

## Промпт 1.4 — Pydantic v2 схемы

**Дата:** 2026-05-15

**Промпт:**
```
Создай Pydantic v2 схемы.

auth.py: UserRegister (username min 3, password validator: буква+цифра+min 8 символов),
Token, UserResponse (from_attributes, без пароля).

account.py: AccountCreate (account_type Literal, initial_deposit Decimal ge=0),
AccountUpdate (все Optional), AccountResponse (from_attributes + created_at).

card.py: CardCreate (account_id, cardholder_name min 2, expiry_date Date, card_type Literal),
CardResponse (from_attributes).

transfer.py: TransferCreate (from_account_id, to_account_id, amount gt=0),
TransferResponse; PaymentCreate (account_id, amount gt=0, recipient min 2),
PaymentResponse.

transaction.py: TransactionResponse (from_attributes, все поля).

schemas/__init__.py экспортирует все классы.
Коммит: «feat(schemas): add Pydantic v2 schemas with validators».
```

**Результат:** Реализованы 5 файлов схем + `__init__.py`. `@field_validator` на `password` (буква + цифра + длина ≥ 8). `@field_validator` на `username` (длина ≥ 3). `Decimal` с `decimal_places=2` для всех денежных полей. Все 13 классов экспортируются через `schemas/__init__.py`.

---

## Промпт 1.5 — Сервисный слой

**Дата:** 2026-05-15

**Промпт:**
```
Ты — senior Python разработчик. Реализуй сервисный слой.

auth_service.py: register (проверка уникальности → 409, hash_password),
authenticate (get_by_username → 401, verify_password → 401, is_active → 403),
create_token (JWT с sub+role).

account_service.py: open_account (генерация уникального 20-значного account_number,
initial_deposit → transaction с типом credit), get_account (404/403),
update_account, close_account (409 если balance > 0 → soft delete is_active=False).

card_service.py: issue_card (проверка owner_id → 403, генерация 16-значного card_number),
get_card (404/403), block_card (409 если уже заблокирована), unblock_card, delete_card.

transfer_service.py: transfer (400 если same account, 403 от чужого счёта, 400 если
недостаточно средств; дебет source + кредит destination + 2 транзакции с общим
reference_id), get_transfers, make_payment (дебет счёта + transaction payment),
get_payments.

Коммит: «feat(services): add business logic layer for banking operations».
```

**Результат:** Реализованы 4 сервисных файла + `__init__.py`. Полная валидация: 400/403/404/409 на все граничные случаи. Генерация `uuid`-based `reference_id` для связки пар транзакций перевода. Метод `close_account` — мягкое удаление (is_active=False). Все импорты проверены.

---

## Промпт 1.6 — API роутеры

**Дата:** 2026-05-15

**Промпт:**
```
Ты — senior Python разработчик. Реализуй API роутеры.

auth.py (prefix=/auth): POST /register (201), POST /login (OAuth2PasswordRequestForm),
GET /me.

accounts.py (prefix=/accounts): GET / (список своих счетов), POST / (201),
GET /{id}, PUT /{id}, DELETE /{id} (204, soft close).

cards.py (prefix=/cards): GET / (все карты пользователя), POST / (201),
GET /{id}, PATCH /{id}/block, PATCH /{id}/unblock, DELETE /{id} (204).

transfers.py: transfers_router (prefix=/transfers): POST / (201), GET / (by account_id);
payments_router (prefix=/payments): POST / (201), GET / (by account_id).

history.py (prefix=/history): GET /{account_id} (с skip/limit pagination).

Docstring на каждый эндпоинт, response_model везде.
Коммит: «feat(api): add all REST API routers».
```

**Результат:** Реализованы 5 файлов роутеров, 22 API-эндпоинта. Все эндпоинты используют `Depends(get_current_active_user)` для защиты. История с `skip`/`limit` pagination через `Query`. Transfers и payments — два отдельных роутера в одном файле.

---

## Промпт 1.7 — Инфраструктура (Alembic, Docker)

**Дата:** 2026-05-15

**Промпт:**
```
Ты — DevOps инженер. Настрой инфраструктуру.

1. Alembic: alembic.ini (без хардкода URL), alembic/env.py (DATABASE_URL из os.environ,
   target_metadata=Base.metadata, asyncio.run + AsyncEngine, импорт всех моделей).

2. Dockerfile multi-stage: builder (python:3.12-slim, pip install),
   runtime (non-root appuser, COPY site-packages, EXPOSE 8000,
   ENTRYPOINT: alembic upgrade head + uvicorn).

3. docker-compose.yml: db (postgres:16-alpine, healthcheck pg_isready, volume postgres_data),
   app (build, env_file, depends_on service_healthy).

4. scripts/seed_db.py: 1 admin + 5 клиентов через Faker, каждому по 1 счёту,
   idempotent (проверка существования admin), asyncio + AsyncSession.

Коммит: «feat(infra): add Alembic, Docker config, and seed script».
```

**Результат:** `alembic.ini` без `sqlalchemy.url`. `alembic/env.py` с async engine и импортом всех 4 моделей. Dockerfile: 2-stage (builder+runtime), useradd appuser, ENTRYPOINT с alembic+uvicorn. `docker-compose.yml`: healthcheck + `depends_on: service_healthy`. `seed_db.py`: admin + 5 клиентов с счетами через Faker, idempotent.

---

## Промпт 2.1 — Тестовое окружение (conftest.py)

**Дата:** 2026-05-15

**Промпт:**
```
Ты — senior Python разработчик. Настрой тестовое окружение.

tests/conftest.py: async pytest-фикстуры (asyncio_mode=auto):
async_engine (function-scope, SQLite in-memory + StaticPool, create_all/drop_all),
async_session, client (override get_db + AsyncClient с ASGITransport),
make_user() (plain async helper — создаёт User через user_repository.create()),
test_user/test_user2 (function-scope),
get_auth_headers() (sync helper, возвращает Bearer-заголовок),
test_account/test_account2 (function-scope, прямые вставки через account_repository).

Добавь asyncio_default_fixture_loop_scope="function" в pyproject.toml.
Коммит: «test(config): add pytest fixtures and test database configuration».
```

**Результат:** Реализован `tests/conftest.py` (110 строк): `os.environ.setdefault` для `DATABASE_URL` и `SECRET_KEY` перед импортами; `async_engine` с `StaticPool` + `create_all/drop_all`; `async_session`; `client` с `dependency_overrides[get_db]`; `make_user()` factory; 2 пользовательских фикстуры; `get_auth_headers()`; `test_account`/`test_account2` через прямые вставки. `pyproject.toml` дополнен `asyncio_default_fixture_loop_scope="function"`.

---

## Промпт 2.2 — Тесты аутентификации

**Дата:** 2026-05-15

**Промпт:**
```
Ты — senior Python разработчик. Напиши тесты для модуля аутентификации.
Формат имён: test_[что_тестируем]_[условие]_[ожидаемый результат].
tests/test_auth.py — минимум 10 тестов:
- register с валидными данными → 201, body содержит id/username, нет пароля
- register с дублированным username → 409
- register с дублированным email → 409
- register с паролем без цифры → 422
- register с паролем без буквы → 422
- register с коротким username → 422
- login с верными данными → 200, есть access_token
- login с неверным паролем → 401
- login с несуществующим пользователем → 401
- GET /me с валидным токеном → 200
- GET /me без токена → 401
- GET /me с невалидным токеном → 401
Faker для уникальных данных. Коммит: «test(auth): add authentication tests».
```

**Результат:** Создан `tests/test_auth.py` (12 тестов, ~90 строк). Вспомогательная функция `_reg(**overrides)` строит валидный payload. `fake.unique.user_name()` и `fake.unique.email()` для уникальности внутри test-сессии. Login использует form data (OAuth2PasswordRequestForm). Все 12 тестов атомарны — каждый получает свежую in-memory SQLite.

---

## Промпт 2.3 — Тесты счетов

**Дата:** 2026-05-15

**Промпт:**
```
Ты — senior Python разработчик. Напиши тесты для управления счетами.
tests/test_accounts.py — минимум 10 тестов:
- list_accounts возвращает свои счета
- open_account → 201, account_number = 20 цифр
- open_account с initial_deposit → balance = deposit
- get_account по ID → 200
- get_account с несуществующим ID → 404
- get_account чужого пользователя → 403
- update_account currency → 200
- close_account с нулевым балансом → 204
- close_account с ненулевым балансом → 409
- open_account без авторизации → 401
Коммит: «test(accounts): add account management tests».
```

**Результат:** Создан `tests/test_accounts.py` (10 тестов, ~80 строк). Тест close с балансом: использует `test_account` с 10 000 RUB → 409. Тест close с нулём: создаёт свежий счёт с `initial_deposit=0.00` → 204. Тест 403: пытается получить счёт `test_user` от `test_user2`.

---

## Промпт 2.4 — Тесты карт и переводов

**Дата:** 2026-05-15

**Промпт:**
```
Ты — senior Python разработчик. Напиши тесты для карт и переводов.
tests/test_cards.py — минимум 8 тестов:
- issue_card → 201, card_number 16 цифр, is_blocked=False
- issue_card для чужого счёта → 403
- issue_card для несуществующего счёта → 404
- get_card → 200
- block_card → 200, is_blocked=True
- block уже заблокированной → 409
- unblock_card → 200, is_blocked=False
- delete_card → 204
- get несуществующей карты → 404

tests/test_transfers.py — минимум 8 тестов:
- transfer → 201, сумма списана с источника
- transfer с недостаточными средствами → 400
- transfer на тот же счёт → 400
- transfer на несуществующий счёт → 404
- transfer с чужого счёта → 403
- payment → 201, баланс уменьшился
- payment с недостаточными средствами → 400
- payment с amount=0 → 422
Коммит: «test(cards,transfers): add card and transfer tests».
```

**Результат:** Создан `tests/test_cards.py` (9 тестов) и `tests/test_transfers.py` (8 тестов). В тестах переводов используется `make_user()` + `account_repository.create()` для создания второго счёта прямо внутри теста — без зависимости от фикстуры. Тест списания баланса: проверяет баланс через GET /accounts/{id} после перевода.

---

## Промпт 2.5 — Тесты истории

**Дата:** 2026-05-15

**Промпт:**
```
Напиши тесты для истории транзакций.
tests/test_history.py:
- history для своего счёта → 200, list
- history для чужого счёта → 403
- history записывает платёж (тип payment в transactions)
- history без auth → 401
- GET /health → 200, status=ok
Также запусти pytest --cov и сохрани отчёт в docs/COVERAGE_REPORT.txt.
Коммит: «test(history): add history tests, achieve ≥70% coverage».
```

**Результат:** Создан `tests/test_history.py` (5 тестов). Тест `test_history_records_payment_transaction` создаёт платёж через POST /payments/, затем проверяет, что в истории присутствует транзакция с `transaction_type = "payment"`. Запущен pytest —  все тесты прошли, покрытие ≥ 70%. Отчёт сохранён в `docs/COVERAGE_REPORT.txt`.

---

## Промпт 3.1 — Намеренно плохой код (Задание 3)

**Дата:** 2026-05-15

**Промпт:**
```
Напиши функцию расчёта комиссии за перевод С НАМЕРЕННЫМИ ОШИБКАМИ для учебного
code review. app/services/bad_commission.py с функцией calc(a, b, c, d),
содержащей 10 проблем:
1) SQL-инъекция (f-строка с аргументами в SQL — 3 места)
2) Захардкоженные credentials (DB_PASSWORD прямо в коде)
3) Функция > 50 строк без разбивки
4) Синхронный блокирующий I/O (requests.get, time.sleep) в async-функции
5) Дублирование расчёта комиссии (5 раз)
6) Магические числа (0.03, 0.1, 0.15, 500, 1000000)
7) float для денег
8) Неинформативные имена (a, b, c, d, x, y, z, tmp, data2)
9) Нет type hints
10) Нет docstring/комментариев
Код должен выглядеть реально. Коммит: «feat(review-exercise): add intentionally flawed code».
```

**Результат:** Создан `app/services/bad_commission.py` (~50 строк). Все 10 проблем реализованы: `psycopg2.connect` с хардкодом пароля, 3 SQL f-строки с инъекцией, расчёт `b * 0.03` в 5 местах, `time.sleep(2)` + `requests.get` внутри async-функции, имена `a/b/c/d/x/y/z/tmp/res/data2`, нет type hints и docstring.

---

## Промпт 3.2 — Code Review и рефакторинг (Задания 3 и 8)

**Дата:** 2026-05-15

**Промпт:**
```
Ты — senior Python разработчик. Проведи детальный code review
app/services/bad_commission.py. Для каждой проблемы: тип, цитата кода,
объяснение последствий, исправление. Найди минимум 5 проблем разных типов.

Создай исправленную версию commission_service.py: PEP 8, type hints, fully async,
httpx вместо requests, ORM без SQL-инъекций, Decimal для денег, SRP (приватные функции),
именованные Final-константы, dataclass(frozen=True) для результата, docstrings.

Сохрани отчёт в docs/CODE_REVIEW_REPORT.md.
Коммиты: «docs(review): add code review report»,
«refactor(commission): replace bad_commission with clean commission_service».
```

**Результат:** Найдено и задокументировано 10 проблем: 4×Critical (3 SQL-инъекции + захардкоженные секреты), 2×High (sync I/O в async, нет обработки ошибок), 2×Medium (дублирование, магические числа + float), 2×Low (имена, type hints). `commission_service.py` (115 строк): `CommissionResult` dataclass, 5 `Final` констант, 5 приватных хелперов, `httpx.AsyncClient` с timeout, ORM `select()` без f-строк, полные type hints и docstrings. `docs/CODE_REVIEW_REPORT.md` содержит таблицу severity и детальный разбор каждой проблемы.

---

## Промпт 4.1 — SQL-запросы (Задание 9)

**Дата:** 2026-05-15

**Промпт:**
```
На основе модели данных банковского приложения (таблицы: users, accounts, transactions)
напиши SQL-запрос, который показывает топ-10 клиентов по сумме исходящих переводов
за последние 30 дней. В результат включи: ФИО клиента, email, количество переводов,
общую сумму, средний размер перевода. Объясни логику запроса.
Также напиши 3 дополнительных аналитических запроса для банка:
- ежемесячный оборот по типам транзакций за текущий год
- счета с нулевым или отрицательным балансом
- среднее время между транзакциями (активность клиентов)
Сохрани в sql/analytics.sql.
Коммит: «feat(sql): add analytical queries for banking reporting».
```

**Результат:** Создан `sql/analytics.sql` с 4 запросами. Запрос 1 использует JOIN users→accounts→transactions с GROUP BY и ORDER BY total_transferred DESC LIMIT 10. Запрос 2 использует `DATE_TRUNC('month', ...)` для группировки по месяцам. Запрос 3 фильтрует `balance <= 0`. Запрос 4 вычисляет среднее время через `EXTRACT(EPOCH FROM ...)`. Каждый запрос снабжён комментарием с объяснением логики.

---

## Промпт 4.2 — Регулярные выражения (Задание 10)

**Дата:** 2026-05-15

**Промпт:**
```
Сгенерируй регулярные выражения для валидации банковских реквизитов:
1) Номер счёта — ровно 20 цифр (российский банковский счёт).
2) Номер карты — 16 цифр, может разделяться пробелами или дефисами группами по 4.
3) Российский телефон — +7 или 8, затем ровно 10 цифр.
Также сгенерируй Python-скрипт для тестирования каждого регулярного выражения
на наборе из 5 валидных и 5 невалидных примеров с подробным выводом.
Сохрани в scripts/regex_validation.py.
Коммит: «feat(scripts): add regex validation for banking requisites».
```

**Результат:** Создан `scripts/regex_validation.py`. Три regex: `^\d{20}$` (счёт), `^(\d{4}[\s-]?){3}\d{4}$` (карта с разделителями), `^(\+7|8)\d{10}$` (телефон). Функция `run_tests()` выводит цветные статусы (✅/❌) для каждого примера и итоговый результат. 30 тест-кейсов: все прошли успешно.

---

## Промпт 5.1 — GitHub Actions CI Pipeline (Задание 4 частично)

**Дата:** 2026-05-15

**Промпт:**
```
Ты — DevOps инженер. Создай GitHub Actions workflow .github/workflows/ci.yml:
name=CI Pipeline, on push/PR к main/master/develop.
Jobs:
- lint: ruff check app/ tests/ + mypy app/ --ignore-missing-imports
- test: pip install -e ".[dev]", pytest --cov=app --cov-report=xml
  --cov-report=term-missing --cov-fail-under=70, codecov/codecov-action@v4
- security: bandit -r app/ -ll --exclude app/services/bad_commission.py
- docker-build: docker build -t bank-app:test .
Добавь env для test-job: DATABASE_URL sqlite+aiosqlite + SECRET_KEY.
Коммит: «ci: add GitHub Actions CI pipeline».
```

**Результат:** Создан `.github/workflows/ci.yml` с 4 независимыми jobs. В test-job добавлены `env: DATABASE_URL/SECRET_KEY` для работы без PostgreSQL. Bandit исключает `bad_commission.py` (намеренно плохой код). Codecov upload без токена (публичный репозиторий).

---

## Промпт 5.2 — AI Code Review Workflow

**Дата:** 2026-05-15

**Промпт:**
```
Ты — DevOps инженер. Создай .github/workflows/ai_review.yml для AI code review при PR.
on: pull_request types=[opened, synchronize] branches=[master, main].
Job: permissions pull-requests=write, checkout fetch-depth=0,
Get PR diff (git diff origin/base...HEAD → pr_diff.txt),
AI Code Review via Gemini API (python3 << 'PYEOF': pip install google-genai,
genai.Client(api_key), client.models.generate_content(model="gemini-2.5-flash"),
сохранить в review_comment.txt),
Post review comment (actions/github-script@v7, createComment).
Промпт для Gemini: структурированное ревью на русском с разделами
Баги/Безопасность/Хорошие практики/Итог.
Коммит: «ci(ai-review): add AI code review workflow for Pull Requests».
```

**Результат:** Создан `.github/workflows/ai_review.yml`. Шаг Get PR diff с `cat pr_diff.txt` для отладки. Python-скрипт: валидация `GEMINI_API_KEY`, diff обрезается до 8000 символов, `google-genai` клиент с моделью `gemini-2.5-flash`, ответ сохраняется в `review_comment.txt`. Шаг Post comment с try/catch для чтения файла. Все шаги с `if: always()` чтобы не пропускались.

---

## Промпт 5.3 — Финальный README (Задание 6)

**Дата:** 2026-05-15

**Промпт:**
```
Ты — технический писатель. Создай README.md для банковского приложения.
Разделы: О проекте (таблица функционала), Архитектура (ASCII-диаграмма слоёв),
Стек технологий (таблица), Запуск Docker (5 шагов) и локальный (7 шагов),
Переменные окружения (таблица с флагом обязательности), API Эндпоинты
(по разделам с методом/путём/описанием + пример POST /transfers),
Запуск тестов, Структура проекта (дерево), Лабораторные задания (1-10), CI/CD.
Коммит: «docs: add comprehensive README».
```

**Результат:** Создан `README.md`. Разделы: заголовок с CI badge, ASCII-диаграмма 4-слойной архитектуры, таблица стека (10 технологий), пошаговые инструкции запуска (Docker + local), таблица env-переменных (7 строк), таблицы эндпоинтов по 6 модулям, пример запроса/ответа POST /transfers, команды pytest, дерево структуры проекта, описание 10 заданий со ссылками на файлы, описание CI/CD с таблицей jobs.
