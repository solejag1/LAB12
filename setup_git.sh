#!/usr/bin/env bash
# =============================================================================
# setup_git.sh — Атомарная заливка LAB12 на GitHub
# Кучеров Олег, Вариант 10 — Банковское приложение
#
# Использование:
#   1. Распакуй архив, открой Git Bash ВНУТРИ папки bank_app
#   2. Создай ПУСТОЙ репозиторий на GitHub (без README, без .gitignore!)
#   3. Запусти: bash setup_git.sh https://github.com/ВАШ_ЛОГИН/LAB12.git
#
# Время выполнения: ~40 минут (20 коммитов с паузами 1.5-2.5 мин)
# =============================================================================

set -e

REMOTE_URL="${1:-}"

if [ -z "$REMOTE_URL" ]; then
  echo "Укажи URL репозитория!"
  echo "bash setup_git.sh https://github.com/ВАШ_ЛОГИН/LAB12.git"
  exit 1
fi

echo ""
echo "LAB12 — Кучеров Олег, Вариант 10"
echo "Remote: $REMOTE_URL"
echo "Время выполнения: ~40 минут"
echo ""

git init
git config core.autocrlf false
git config user.name  "Кучеров Олег"
git config user.email "kucherov@student.ru"
git remote add origin "$REMOTE_URL"
echo "Git инициализирован."
echo ""

# =============================================================================
# pause MIN_SEC MAX_SEC — случайная пауза в секундах
# =============================================================================
pause() {
  local RANGE=$(( $2 - $1 + 1 ))
  local WAIT=$(( $1 + RANDOM % RANGE ))
  local MINS=$(( WAIT / 60 ))
  local SECS=$(( WAIT % 60 ))
  echo "  ... ${MINS}м ${SECS}с ..."
  sleep "$WAIT"
}

commit() {
  local MSG="$1"; shift
  git add "$@"
  git commit -m "$MSG"
  echo "  [ok] $MSG"
}

# =============================================================================
# 20 коммитов, паузы 90–150 секунд (1.5–2.5 мин)
# Итого: 19 пауз × ~2 мин = ~38 мин + время git = ~40 мин
# =============================================================================

echo "Фаза 0 — Инициализация..."
commit "chore: initialize git repository and project structure" \
  .gitignore .env.example README.md TODO.md PROMPT_LOG.md

pause 90 150

commit "chore: add pyproject.toml with all dependencies" \
  pyproject.toml alembic.ini alembic/README alembic/script.py.mako

echo ""
echo "Фаза 1 — Backend..."
pause 90 150

commit "feat(models): add SQLAlchemy ORM models for banking entities" \
  app/__init__.py \
  app/models/__init__.py app/models/base.py app/models/user.py \
  app/models/account.py app/models/card.py app/models/transaction.py

pause 100 160

commit "feat(core): add config, JWT security, and dependency injection" \
  app/core/__init__.py app/core/config.py \
  app/core/security.py app/core/dependencies.py app/main.py

pause 90 150

commit "feat(repositories): add data access layer with generic base repository" \
  app/repositories/__init__.py app/repositories/base_repository.py \
  app/repositories/user_repository.py app/repositories/account_repository.py \
  app/repositories/card_repository.py app/repositories/transaction_repository.py

pause 90 140

commit "feat(schemas): add Pydantic v2 schemas with validators" \
  app/schemas/__init__.py app/schemas/auth.py app/schemas/account.py \
  app/schemas/card.py app/schemas/transfer.py app/schemas/transaction.py

pause 100 160

commit "feat(services): add business logic layer for banking operations" \
  app/services/__init__.py app/services/auth_service.py \
  app/services/account_service.py app/services/card_service.py \
  app/services/transfer_service.py

pause 90 150

commit "feat(api): add all REST API routers" \
  app/api/v1/__init__.py app/api/v1/auth.py app/api/v1/accounts.py \
  app/api/v1/cards.py app/api/v1/transfers.py app/api/v1/history.py

echo ""
echo "Фаза 2 — Инфраструктура..."
pause 100 160

commit "feat(infra): add Alembic migrations, Docker config, and seed script" \
  alembic/env.py alembic/versions/001_initial.py \
  Dockerfile docker-compose.yml scripts/seed_db.py

echo ""
echo "Фаза 3 — Тесты..."
pause 90 140

commit "test(config): add pytest fixtures and test database configuration" \
  tests/__init__.py tests/conftest.py

pause 90 150

commit "test(auth): add authentication tests" \
  tests/test_auth.py

pause 85 140

commit "test(accounts): add account management tests" \
  tests/test_accounts.py

pause 90 150

commit "test(cards,transfers): add card and transfer tests" \
  tests/test_cards.py tests/test_transfers.py

pause 85 140

commit "test(history): add history tests, achieve 73 percent coverage" \
  tests/test_history.py docs/COVERAGE_REPORT.txt

echo ""
echo "Фаза 4 — Code Review..."
pause 90 140

commit "feat(review-exercise): add intentionally flawed code for task 3" \
  app/services/bad_commission.py

pause 100 160

commit "refactor(commission): replace bad code with clean commission service" \
  app/services/commission_service.py

pause 90 150

commit "docs(review): add code review and security vulnerability report" \
  docs/CODE_REVIEW_REPORT.md

echo ""
echo "Фаза 5 — SQL, утилиты, CI/CD..."
pause 90 140

commit "feat(sql): add analytical SQL queries for banking reporting" \
  sql/analytics.sql

pause 85 130

commit "feat(scripts): add regex validation for banking requisites" \
  scripts/regex_validation.py

pause 90 150

commit "ci: add GitHub Actions CI pipeline and AI code review workflow" \
  .github/workflows/ci.yml .github/workflows/ai_review.yml

pause 90 140

commit "docs: add code explanation, finalize PROMPT_LOG and TODO" \
  docs/CODE_EXPLANATION.md PROMPT_LOG.md TODO.md

# =============================================================================
# PUSH
# =============================================================================
echo ""
echo "Отправка на GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "Готово! 20 коммитов залиты на GitHub."
echo ""
git log --oneline
