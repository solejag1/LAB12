# TODO.md — План разработки

**Студент:** Кучеров Олег  
**Вариант:** 10 — Банковское приложение  
**Лабораторная работа:** №12, AI-ассистированная разработка

---

## 🗂️ Agentic Workflow

Ниже представлен план разработки с атомарными задачами.
Каждая задача соответствует одному коммиту в git-истории.

---

## Фаза 0 — Инициализация проекта

- [x] 0.1 Инициализировать git-репозиторий, создать файловую структуру (`chore: initialize git repository and project structure`)
- [x] 0.2 Добавить `.gitignore` и `.env.example` (`chore: add .gitignore and .env.example`)
- [x] 0.3 Создать `pyproject.toml` со всеми зависимостями и инструментами (`chore: add pyproject.toml with all dependencies`)

---

## Фаза 1 — Backend: ядро приложения

### Задание 1 — CRUD-приложение
- [x] 1.1 Реализовать ORM-модели: `User`, `Account`, `Card`, `Transaction`, `Base`, `TimestampMixin` (`feat(models): add SQLAlchemy ORM models for banking entities`)
- [x] 1.2 Реализовать core-слой: `config.py`, `security.py` (JWT + bcrypt), `dependencies.py` (`feat(core): add config, JWT security, and dependency injection`)
- [x] 1.3 Реализовать репозитории: `BaseRepository`, `UserRepository`, `AccountRepository`, `CardRepository`, `TransactionRepository` (`feat(repositories): add data access layer with generic base repository`)
- [x] 1.4 Реализовать Pydantic v2 схемы с валидацией (`feat(schemas): add Pydantic v2 schemas with validators`)
- [x] 1.5 Реализовать сервисный слой: `AuthService`, `AccountService`, `CardService`, `TransferService` (`feat(services): add business logic layer for banking operations`)
- [x] 1.6 Реализовать API роутеры: auth, accounts, cards, transfers, payments, history (`feat(api): add all REST API routers`)

### Задание 7 — Миграции БД
- [x] 1.7 Настроить Alembic и Docker: `alembic.ini`, `env.py`, `Dockerfile`, `docker-compose.yml`, `seed_db.py`, миграция `001_initial.py` (`feat(infra): add Alembic, Docker config, and seed script`)

---

## Фаза 2 — Тестирование

### Задание 2 — Генерация тестов
- [x] 2.1 Настроить `conftest.py`: in-memory SQLite, фикстуры, dependency override (`test(config): add pytest fixtures and test database configuration`)
- [x] 2.2 Написать тесты аутентификации (12 тестов) (`test(auth): add authentication tests`)
- [x] 2.3 Написать тесты счетов (10 тестов) (`test(accounts): add account management tests`)
- [x] 2.4 Написать тесты карт (9 тестов) и переводов (8 тестов) (`test(cards,transfers): add card and transfer tests`)
- [x] 2.5 Написать тесты истории (5 тестов), достичь покрытия ≥ 70% (`test(history): add history tests, achieve ≥70% coverage`)

---

## Фаза 3 — Code Review и рефакторинг

### Задание 3 — Рефакторинг плохого кода
- [x] 3.1 Написать намеренно плохую функцию `bad_commission.py` (10 антипаттернов) (`feat(review-exercise): add intentionally flawed code`)
- [x] 3.2 Провести code review, написать `commission_service.py`, создать `docs/CODE_REVIEW_REPORT.md` (`docs(review): add code review report`)

---

## Фаза 4 — Аналитика и утилиты

### Задание 9 — SQL-запросы
- [x] 4.1 Написать аналитические SQL-запросы (топ клиентов, оборот по месяцам, нулевые балансы, активность) и сохранить в `sql/analytics.sql` (`feat(sql): add analytical queries for banking reporting`)

### Задание 10 — Регулярные выражения
- [x] 4.2 Написать регулярные выражения для валидации реквизитов и тестовый скрипт `scripts/regex_validation.py` (`feat(scripts): add regex validation for banking requisites`)

---

## Фаза 5 — CI/CD и документация

### Задание 4 — Docker + CI/CD
- [x] 5.1 Создать CI Pipeline `.github/workflows/ci.yml` (lint, tests, security, docker-build) (`ci: add GitHub Actions CI pipeline`)
- [x] 5.2 Создать AI Code Review `.github/workflows/ai_review.yml` (Gemini, PR comment) (`ci(ai-review): add AI code review workflow for Pull Requests`)

### Задание 6 — Документация
- [x] 5.3 Написать полный `README.md` с архитектурой, API-справочником и инструкциями (`docs: add comprehensive README`)

### Задание 5 — Объяснение кода
- [x] 5.4 Создать `docs/CODE_EXPLANATION.md` с разбором сложной функции (`docs: add code explanation for commission calculation`)

### Задание 8 — Уязвимости (объединено с задачей 3.2)
- [x] 5.5 Обновить `docs/CODE_REVIEW_REPORT.md`, добавив раздел по уязвимостям безопасности (`docs(security): document security vulnerabilities and fixes`)

---

## Фаза 6 — Финализация

- [x] 6.1 Обновить `PROMPT_LOG.md` — задокументировать все промпты и ответы ИИ (`docs: update PROMPT_LOG with all prompts and AI responses`)
- [x] 6.2 Обновить `TODO.md` — отметить все выполненные задачи (`docs: update TODO with final status`)
- [x] 6.3 Финальный прогон `pytest --cov`, проверить покрытие ≥ 70% (`test: final coverage check`)
- [x] 6.4 Финальный `ruff check app/ tests/` и `bandit -r app/` — нет критических ошибок (`chore: final linting and security check`)

---

## 📊 Статус задания

| Задание | Описание | Файлы | Статус |
|---------|----------|-------|--------|
| 1 | CRUD-приложение | `app/` (все модули) | ✅ |
| 2 | Тесты pytest ≥ 70% | `tests/` | ✅ |
| 3 | Рефакторинг плохого кода | `bad_commission.py`, `commission_service.py` | ✅ |
| 4 | Docker + CI/CD | `Dockerfile`, `docker-compose.yml`, `.github/` | ✅ |
| 5 | Объяснение кода | `docs/CODE_EXPLANATION.md` | ✅ |
| 6 | Документация README | `README.md` | ✅ |
| 7 | Миграции Alembic | `alembic/versions/001_initial.py` | ✅ |
| 8 | Поиск уязвимостей | `docs/CODE_REVIEW_REPORT.md` | ✅ |
| 9 | SQL-запросы | `sql/analytics.sql` | ✅ |
| 10 | Регулярные выражения | `scripts/regex_validation.py` | ✅ |
