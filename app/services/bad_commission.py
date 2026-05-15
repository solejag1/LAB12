"""
Задание 3. Намеренно плохой код для учебного code review.
Функция расчёта комиссии за перевод — содержит типичные антипаттерны.
"""
import requests
import time


# Задание 3: Плохой код (намеренно) — для последующего рефакторинга
async def calc(a, b, c, d):
    # соединение с базой
    import psycopg2
    conn = psycopg2.connect("host=localhost user=postgres password=supersecret123 dbname=bank")
    cur = conn.cursor()

    # получить данные счета
    cur.execute("SELECT balance FROM accounts WHERE id = " + str(a))
    res = cur.fetchone()
    x = res[0]

    # проверить тип
    cur.execute("SELECT account_type FROM accounts WHERE id = " + str(a))
    tmp = cur.fetchone()
    y = tmp[0]

    # считаем комиссию
    if d == "PROMO10":
        z = b * 0.03
        z = z - z * 0.1
    elif d == "PROMO15":
        z = b * 0.03
        z = z - z * 0.15
    elif d == "VIP":
        z = b * 0.03
        z = z - z * 0.15
    else:
        z = b * 0.03

    # скидка за тип счёта
    if y == "savings":
        z = b * 0.03
        z = z - z * 0.05
    if y == "credit":
        z = b * 0.03
        z = z - z * 0.05

    # проверить лимит
    if b > 1000000:
        z = z + 500
    if b > 500000:
        z = z + 100

    # запрос к внешнему сервису (блокирующий!)
    time.sleep(2)
    r = requests.get("http://commission-service/api/verify?amount=" + str(b) + "&code=" + str(d))
    data2 = r.json()

    # логируем транзакцию
    cur.execute("INSERT INTO transaction_log (account_id, amount, commission, promo) VALUES ("
                + str(a) + ", " + str(b) + ", " + str(z) + ", '" + str(d) + "')")
    conn.commit()
    cur.close()
    conn.close()

    return z
