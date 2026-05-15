-- Задание 9. Аналитические SQL-запросы для банковского приложения.
-- Промпт: «На основе модели данных банковского приложения (таблицы: users, accounts,
-- transactions) напиши SQL-запрос, который показывает топ-10 клиентов по сумме
-- исходящих переводов за последние 30 дней. В результат включи: ФИО клиента,
-- email, количество переводов, общую сумму переводов, средний размер перевода.
-- Объясни логику запроса.»

-- ─────────────────────────────────────────────────────────────────────────────
-- Запрос 1: Топ-10 клиентов по сумме исходящих переводов за 30 дней
-- ─────────────────────────────────────────────────────────────────────────────
-- Логика:
--   1. Из таблицы transactions берём строки с типом transfer_out
--      и статусом completed за последние 30 дней.
--   2. JOIN с accounts чтобы получить owner_id счёта.
--   3. JOIN с users чтобы получить ФИО и email клиента.
--   4. GROUP BY по пользователю — считаем агрегаты.
--   5. ORDER BY суммарной сумме переводов по убыванию, LIMIT 10.

SELECT
    u.full_name                          AS client_name,
    u.email                              AS email,
    COUNT(t.id)                          AS transfer_count,
    SUM(t.amount)                        AS total_transferred,
    ROUND(AVG(t.amount), 2)              AS avg_transfer_amount
FROM transactions t
JOIN accounts a  ON t.account_id = a.id
JOIN users u     ON a.owner_id   = u.id
WHERE
    t.transaction_type = 'transfer_out'
    AND t.status        = 'completed'
    AND t.created_at   >= NOW() - INTERVAL '30 days'
GROUP BY
    u.id, u.full_name, u.email
ORDER BY
    total_transferred DESC
LIMIT 10;


-- ─────────────────────────────────────────────────────────────────────────────
-- Запрос 2: Ежемесячный оборот по типам транзакций за текущий год
-- ─────────────────────────────────────────────────────────────────────────────
-- Объяснение ИИ: DATE_TRUNC усекает дату до начала месяца, что позволяет
-- группировать все транзакции в рамках одного месяца независимо от дня.

SELECT
    DATE_TRUNC('month', t.created_at)   AS month,
    t.transaction_type,
    COUNT(t.id)                          AS operation_count,
    SUM(t.amount)                        AS total_amount
FROM transactions t
WHERE
    t.status = 'completed'
    AND EXTRACT(YEAR FROM t.created_at) = EXTRACT(YEAR FROM NOW())
GROUP BY
    month, t.transaction_type
ORDER BY
    month ASC, total_amount DESC;


-- ─────────────────────────────────────────────────────────────────────────────
-- Запрос 3: Счета с отрицательным балансом или нулевым балансом
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    a.account_number,
    a.account_type,
    a.balance,
    a.currency,
    u.full_name  AS owner,
    u.email
FROM accounts a
JOIN users u ON a.owner_id = u.id
WHERE
    a.is_active = TRUE
    AND a.balance <= 0
ORDER BY
    a.balance ASC;


-- ─────────────────────────────────────────────────────────────────────────────
-- Запрос 4: Среднее время между транзакциями по счёту (активность клиентов)
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    u.full_name,
    a.account_number,
    COUNT(t.id)                                              AS tx_count,
    MIN(t.created_at)                                        AS first_tx,
    MAX(t.created_at)                                        AS last_tx,
    ROUND(
        EXTRACT(EPOCH FROM (MAX(t.created_at) - MIN(t.created_at)))
        / NULLIF(COUNT(t.id) - 1, 0) / 3600,
        1
    )                                                        AS avg_hours_between_tx
FROM transactions t
JOIN accounts a ON t.account_id = a.id
JOIN users    u ON a.owner_id   = u.id
WHERE t.status = 'completed'
GROUP BY u.id, u.full_name, a.id, a.account_number
HAVING COUNT(t.id) > 1
ORDER BY avg_hours_between_tx ASC
LIMIT 20;
