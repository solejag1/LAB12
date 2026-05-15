# 🏦 Banking Application

> Банковское приложение | Лабораторная работа №12, Вариант 10

**Студент:** Кучеров Олег  
**Вариант:** 10 — Банковское приложение

[![CI](https://github.com/your-username/LAB12/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/LAB12/actions/workflows/ci.yml)

---

## 📋 О проекте

REST API для банковского приложения: управление счетами, картами, переводами, платежами и историей операций.

**Ключевые возможности:**

| Модуль | Что умеет |
|--------|-----------|
| Счета | Открытие, пополнение, закрытие, проверка баланса |
| Карты | Выпуск карт, привязка к счёту, блокировка/разблокировка |
| Переводы | Переводы между счетами с валидацией баланса |
| Платежи | Оплата услуг, история транзакций |
| История | Полный лог операций по счёту с фильтрацией |

---

## 🏗️ Архитектура

```
HTTP Request
     │
     ▼
┌─────────────────────────────┐
│   API Layer  (app/api/v1/)  │  FastAPI роутеры — валидация, HTTP
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│  Service Layer (services/)  │  Бизнес-логика, валидация баланса
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│  Repository Layer (repos/)  │  Async CRUD, изолированные SQL
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│  Model Layer (models/)      │  SQLAlchemy 2.0 ORM
└────────────┬────────────────┘
             │
             ▼
        PostgreSQL / SQLite
```

---

## 🛠️ Стек технологий

| Технология | Версия | Назначение |
|------------|--------|------------|
| **Python** | 3.12 | Язык разработки |
| **FastAPI** | ≥ 0.111 | Async REST-фреймворк |
| **SQLAlchemy** | ≥ 2.0 | ORM, async-сессии |
| **PostgreSQL** | 16 | Основная база данных |
| **Alembic** | ≥ 1.13 | Миграции схемы БД |
| **Pydantic v2** | ≥ 2.7 | Схемы запросов/ответов |
| **pytest** | ≥ 8.2 | Тестовый фреймворк |
| **aiosqlite** | ≥ 0.20 | In-memory SQLite для тестов |
| **Docker** | — | Контейнеризация |
| **GitHub Actions** | — | CI/CD |

---

## 🚀 Запуск

### Вариант 1: Docker (рекомендуется)

```bash
git clone https://github.com/your-username/LAB12.git
cd LAB12
cp .env.example .env
docker compose up -d
docker compose exec app python -m scripts.seed_db
```

| Адрес | Описание |
|-------|----------|
| http://localhost:8000 | API |
| http://localhost:8000/docs | Swagger UI |
| http://localhost:8000/redoc | ReDoc |

### Вариант 2: Локальная разработка

```bash
git clone https://github.com/your-username/LAB12.git
cd LAB12
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\Activate.ps1  # Windows
pip install -e ".[dev]"
cp .env.example .env
alembic upgrade head
python -m scripts.seed_db
uvicorn app.main:app --reload --port 8000
```

---

## 🔑 Переменные окружения

| Переменная | Описание | Пример | Обязательная |
|------------|----------|--------|-------------|
| `DATABASE_URL` | Строка подключения | `postgresql+asyncpg://postgres:postgres@db:5432/bank_db` | ✅ |
| `SECRET_KEY` | Секрет для JWT | `change-me-32-char-secret-key!!` | ✅ |
| `ALGORITHM` | Алгоритм JWT | `HS256` | — |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Время жизни токена | `30` | — |
| `POSTGRES_USER` | Пользователь БД | `postgres` | — |
| `POSTGRES_PASSWORD` | Пароль БД | `postgres` | — |
| `POSTGRES_DB` | Имя базы данных | `bank_db` | — |

---

## 📡 API Эндпоинты

### Аутентификация (`/api/v1/auth`)

| Метод | Путь | Описание |
|-------|------|----------|
| `POST` | `/auth/register` | Регистрация клиента |
| `POST` | `/auth/login` | Получение JWT-токена |
| `GET` | `/auth/me` | Профиль текущего пользователя |

### Счета (`/api/v1/accounts`)

| Метод | Путь | Описание |
|-------|------|----------|
| `GET` | `/accounts/` | Список счетов клиента |
| `POST` | `/accounts/` | Открыть новый счёт |
| `GET` | `/accounts/{id}` | Данные счёта |
| `PUT` | `/accounts/{id}` | Обновить счёт |
| `DELETE` | `/accounts/{id}` | Закрыть счёт |

### Карты (`/api/v1/cards`)

| Метод | Путь | Описание |
|-------|------|----------|
| `GET` | `/cards/` | Список карт |
| `POST` | `/cards/` | Выпустить карту |
| `GET` | `/cards/{id}` | Данные карты |
| `PATCH` | `/cards/{id}/block` | Заблокировать карту |
| `PATCH` | `/cards/{id}/unblock` | Разблокировать карту |
| `DELETE` | `/cards/{id}` | Удалить карту |

### Переводы (`/api/v1/transfers`)

| Метод | Путь | Описание |
|-------|------|----------|
| `GET` | `/transfers/` | История переводов |
| `POST` | `/transfers/` | Выполнить перевод |
| `GET` | `/transfers/{id}` | Данные перевода |

### Платежи (`/api/v1/payments`)

| Метод | Путь | Описание |
|-------|------|----------|
| `GET` | `/payments/` | История платежей |
| `POST` | `/payments/` | Совершить платёж |
| `GET` | `/payments/{id}` | Данные платежа |

### История (`/api/v1/history`)

| Метод | Путь | Описание |
|-------|------|----------|
| `GET` | `/history/{account_id}` | История операций по счёту |

**Пример: перевод между счетами**

```json
POST /api/v1/transfers/
Authorization: Bearer <token>
{
  "from_account_id": 1,
  "to_account_id": 2,
  "amount": "5000.00",
  "description": "Оплата аренды"
}
```

```json
{
  "id": 42,
  "from_account_id": 1,
  "to_account_id": 2,
  "amount": "5000.00",
  "status": "completed",
  "description": "Оплата аренды",
  "created_at": "2026-05-13T12:00:00"
}
```

---

## 🧪 Запуск тестов

```bash
pytest
pytest --cov=app --cov-report=term-missing --cov-report=html
pytest tests/test_accounts.py -v
pytest -k "transfer" -v
```

**Текущее покрытие:** ≥ 70%

---

## 📁 Структура проекта

```
bank_app/
├── app/
│   ├── api/v1/
│   │   ├── auth.py          # Аутентификация
│   │   ├── accounts.py      # CRUD счетов
│   │   ├── cards.py         # Управление картами
│   │   ├── transfers.py     # Переводы
│   │   ├── payments.py      # Платежи
│   │   └── history.py       # История операций
│   ├── core/
│   │   ├── config.py        # Настройки
│   │   ├── security.py      # JWT, bcrypt
│   │   └── dependencies.py  # FastAPI Depends
│   ├── models/              # SQLAlchemy ORM-модели
│   ├── repositories/        # Data Access Layer
│   ├── schemas/             # Pydantic v2 схемы
│   ├── services/            # Бизнес-логика
│   └── main.py
├── alembic/                 # Миграции БД
├── tests/                   # pytest тесты
├── scripts/seed_db.py       # Тестовые данные
├── sql/                     # SQL-запросы (Задание 9)
├── docs/
│   ├── CODE_REVIEW_REPORT.md
│   └── COVERAGE_REPORT.txt
├── .github/workflows/
│   ├── ci.yml               # CI Pipeline
│   └── ai_review.yml        # AI Code Review
├── Dockerfile
├── docker-compose.yml
├── PROMPT_LOG.md
└── README.md
```

---

## 🎓 Лабораторные задания

### Задание 1 — CRUD-приложение
Полная реализация REST API «Банковское приложение»: модели Account, Card, Transfer, Payment, Transaction; Pydantic-валидация; обработка ошибок 404/422/409.

### Задание 2 — Тесты
pytest-тесты с покрытием ≥ 70%: CRUD счетов, переводы, карты, граничные случаи (недостаточно средств, несуществующий счёт).

### Задание 3 — Рефакторинг
Намеренно плохая функция расчёта комиссии → рефакторинг с объяснением. Отчёт: `docs/CODE_REVIEW_REPORT.md`.

### Задание 4 — Docker
Dockerfile multi-stage + docker-compose.yml с PostgreSQL и Alembic-миграциями.

### Задание 5 — Объяснение кода
Разбор функции расчёта процентов по кредиту с объяснением ИИ. Файл: `docs/CODE_EXPLANATION.md`.

### Задание 6 — Документация
Этот README.md сгенерирован с помощью ИИ.

### Задание 7 — Миграции БД
Alembic-миграции в `alembic/versions/`.

### Задание 8 — Уязвимости
Анализ кода на SQL-инъекции, незащищённые эндпоинты, отсутствие валидации. Исправления задокументированы в `docs/CODE_REVIEW_REPORT.md`.

### Задание 9 — SQL-запросы
Аналитические запросы в `sql/analytics.sql`.

### Задание 10 — Регулярные выражения
Валидация номера счёта и карты. Файл: `scripts/regex_validation.py`.

---

## ⚙️ CI/CD

### ci.yml — Continuous Integration

| Job | Что проверяет |
|-----|---------------|
| **Lint** | `ruff check app/ tests/` |
| **Tests** | `pytest --cov=app --cov-fail-under=70` |
| **Security** | `bandit -r app/ -ll` |
| **Docker Build** | `docker build -t bank-app:test .` |

### ai_review.yml — AI Code Review

При создании PR автоматически анализирует изменения через Gemini API и оставляет комментарий.

**Настройка:**
1. Получи ключ на [aistudio.google.com/apikey](https://aistudio.google.com/apikey) (бесплатно)
2. GitHub репозиторий → Settings → Secrets → Actions → New secret
3. Name: `GEMINI_API_KEY`, Value: твой ключ
