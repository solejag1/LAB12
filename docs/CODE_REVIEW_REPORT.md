# Code Review Report — bad_commission.py

**Задание 3 и 8. Анализ плохого кода + поиск уязвимостей.**

Файл: `app/services/bad_commission.py`  
Исправленная версия: `app/services/commission_service.py`

---

## Таблица найденных проблем

| № | Тип | Серьёзность | Файл:строка | Описание |
|---|-----|-------------|-------------|----------|
| 1 | SQL-инъекция | 🔴 Critical | `bad_commission.py:15` | f-строка с `str(a)` в SQL-запросе |
| 2 | SQL-инъекция | 🔴 Critical | `bad_commission.py:20` | Второй SQL-запрос тоже уязвим |
| 3 | SQL-инъекция | 🔴 Critical | `bad_commission.py:40` | INSERT с конкатенацией строк — полная инъекция |
| 4 | Захардкоженные учётные данные | 🔴 Critical | `bad_commission.py:9` | Пароль БД прямо в коде |
| 5 | Синхронный блокирующий I/O | 🟠 High | `bad_commission.py:32-34` | `time.sleep(2)` и `requests.get` в async-функции блокируют event loop |
| 6 | Дублирование бизнес-логики | 🟠 High | `bad_commission.py:23-31` | Расчёт `z = b * 0.03` повторяется 5 раз |
| 7 | Магические числа | 🟡 Medium | `bad_commission.py:23-31` | `0.03`, `0.1`, `0.15`, `500`, `1000000` без именованных констант |
| 8 | Float для денег | 🟡 Medium | Везде | `float` вместо `Decimal` приводит к ошибкам округления |
| 9 | Неинформативные имена | 🟡 Medium | Везде | `a`, `b`, `c`, `d`, `x`, `y`, `z`, `tmp`, `data2`, `res` |
| 10 | Отсутствие type hints и docstring | 🟢 Low | `bad_commission.py:7` | Нет аннотаций типов и документации |

---

## Детальный разбор

### 1-3. SQL-инъекции (Critical)

**Что сгенерировал ИИ:**
```python
cur.execute("SELECT balance FROM accounts WHERE id = " + str(a))
```

**В чём проблема:**  
Если `a` содержит `1 OR 1=1`, запрос вернёт все строки таблицы. Злоумышленник может извлечь любые данные или уничтожить таблицы.

**Как исправил:**
```python
result = await db.execute(select(Account).where(Account.id == account_id))
```
ORM через SQLAlchemy использует параметризованные запросы автоматически — инъекция невозможна.

---

### 4. Захардкоженные учётные данные (Critical)

**Что сгенерировал ИИ:**
```python
conn = psycopg2.connect("host=localhost user=postgres password=supersecret123 dbname=bank")
```

**В чём проблема:**  
Пароль попадает в систему контроля версий (git), виден в истории коммитов навсегда. Любой, кто имеет доступ к репозиторию, получает прямой доступ к базе данных.

**Как исправил:**  
Используем переменные окружения через `pydantic-settings` в `app/core/config.py`. Все чувствительные данные хранятся в `.env`, который добавлен в `.gitignore`.

---

### 5. Синхронный I/O в async-функции (High)

**Что сгенерировал ИИ:**
```python
time.sleep(2)
r = requests.get("http://commission-service/api/verify?amount=" + str(b))
```

**В чём проблема:**  
`time.sleep()` и `requests.get()` — блокирующие вызовы. В async-функции они замораживают весь event loop FastAPI, блокируя обработку всех остальных запросов на время ожидания.

**Как исправил:**
```python
async with httpx.AsyncClient(timeout=5.0) as http:
    await http.get(COMMISSION_SERVICE_URL, params={"amount": str(amount)})
```
`httpx.AsyncClient` — неблокирующий async HTTP-клиент. Дополнительно завёрнут в `try/except` — внешний сервис не должен ломать транзакцию.

---

### 6. Дублирование расчёта комиссии (High)

**Что сгенерировал ИИ:**
```python
if d == "PROMO10":
    z = b * 0.03
    z = z - z * 0.1
elif d == "PROMO15":
    z = b * 0.03   # ← снова b * 0.03
    z = z - z * 0.15
elif d == "VIP":
    z = b * 0.03   # ← и снова
    ...
if y == "savings":
    z = b * 0.03   # ← четвёртый раз!
```

**В чём проблема:**  
DRY-нарушение. Ставка `0.03` присваивается на каждой ветке заново — если нужно изменить ставку, придётся менять в 5 местах, легко пропустить.

**Как исправил:**  
Вынес в именованную константу `BASE_COMMISSION_RATE = Decimal("0.03")` и вызываю один раз через `_calculate_base_commission()`.

---

### 7-8. Магические числа и float для денег (Medium)

**Что сгенерировал ИИ:**
```python
z = b * 0.03
if b > 1000000:
    z = z + 500
```

**В чём проблема:**  
`0.03`, `1000000`, `500` — числа без контекста. `float` для денег даёт ошибки типа `0.1 + 0.2 = 0.30000000000000004`.

**Как исправил:**
```python
BASE_COMMISSION_RATE: Final[Decimal] = Decimal("0.03")
HIGH_AMOUNT_THRESHOLD: Final[Decimal] = Decimal("1000000.00")
HIGH_AMOUNT_SURCHARGE: Final[Decimal] = Decimal("500.00")
```

---

## Итог

После рефакторинга `commission_service.py`:
- ✅ Нет SQL-инъекций (используется ORM)
- ✅ Нет захардкоженных секретов
- ✅ Весь I/O асинхронный
- ✅ Нет дублирования кода
- ✅ `Decimal` для всех денежных вычислений
- ✅ Полные type hints и docstring
- ✅ Именованные константы
- ✅ Разделение ответственности (SRP) — 5 приватных функций
