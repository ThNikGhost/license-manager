import sqlite3
from datetime import datetime, timedelta
from DB import get_connection, init_db


# ---------------- Пользователи ---------------- #

def add_user(login: str, password: str):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (login, password, last_login) VALUES (?, ?, ?)",
            (login, password, None)
        )
        conn.commit()


def authenticate_user(login: str, password: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE login = ? AND password = ?", (login, password))
        user = cursor.fetchone()
        if user:
            cursor.execute(
                "UPDATE users SET last_login = ? WHERE id = ?",
                (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user[0])
            )
            conn.commit()
            return True
        return False


def get_users():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, login, last_login FROM users")
        return cursor.fetchall()


# ---------------- Компьютеры ---------------- #

def add_computer(room_number, computer_name):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO computers (room_number, computer_name) VALUES (?, ?)",
            (room_number, computer_name)
        )
        conn.commit()
        return cursor.lastrowid


def get_computers():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM computers")
        return cursor.fetchall()


def delete_computer(computer_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM computers WHERE id = ?", (computer_id,))
        conn.commit()


# ---------------- Лицензии ---------------- #

def add_license(computer_id, software, license_start, license_end, budget):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO licenses (computer_id, software, license_start, license_end, budget)
            VALUES (?, ?, ?, ?, ?)
        """, (computer_id, software, license_start, license_end, budget))
        conn.commit()


def get_licenses(computer_id=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        if computer_id:
            cursor.execute("SELECT * FROM licenses WHERE computer_id = ?", (computer_id,))
        else:
            cursor.execute("SELECT * FROM licenses")
        return cursor.fetchall()


def update_license(license_id, **kwargs):
    """Редактирует данные лицензии (только переданные поля)."""
    if not kwargs:
        return
    with get_connection() as conn:
        cursor = conn.cursor()
        fields = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values()) + [license_id]
        cursor.execute(f"UPDATE licenses SET {fields} WHERE id = ?", values)
        conn.commit()


def delete_license(license_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM licenses WHERE id = ?", (license_id,))
        conn.commit()


def search_licenses(software=None, room=None, active_only=False):
    """
    Поиск лицензий по параметрам:
    - software: название ПО (LIKE)
    - room: номер аудитории
    - active_only: только активные лицензии
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        query = """
            SELECT l.id, c.room_number, c.computer_name, l.software, l.license_start, l.license_end, l.budget
            FROM licenses l
            JOIN computers c ON l.computer_id = c.id
            WHERE 1=1
        """
        params = []

        if software:
            query += " AND l.software LIKE ?"
            params.append(f"%{software}%")

        if room:
            query += " AND c.room_number = ?"
            params.append(room)

        if active_only:
            today = datetime.now().strftime("%Y-%m-%d")
            query += " AND l.license_start <= ? AND l.license_end >= ?"
            params.extend([today, today])

        cursor.execute(query, params)
        return cursor.fetchall()


        # ---------------- Количество лицензий ---------------- #

def count_licenses():
    """Возвращает количество лицензий: активные, истекают через 2 месяца, истекшие."""
    today = datetime.now().date()
    two_months = today + timedelta(days=60)

    with get_connection() as conn:
        cursor = conn.cursor()

        # Активные (сегодня входит в диапазон)
        cursor.execute("""
            SELECT COUNT(*) FROM licenses 
            WHERE license_start <= ? AND license_end >= ?
        """, (today, today))
        active = cursor.fetchone()[0]

        # Истекают в ближайшие 2 месяца
        cursor.execute("""
            SELECT COUNT(*) FROM licenses 
            WHERE license_end > ? AND license_end <= ?
        """, (today, two_months))
        expiring = cursor.fetchone()[0]

        # Истекшие
        cursor.execute("""
            SELECT COUNT(*) FROM licenses 
            WHERE license_end < ?
        """, (today,))
        expired = cursor.fetchone()[0]

    return {"active": active, "expiring": expiring, "expired": expired}


# ---------------- Поиск по имени компьютера ---------------- #

def get_computer_by_name(room_number, computer_name):
    """Получает компьютер по аудитории и имени (уникальная пара)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM computers WHERE room_number = ? AND computer_name = ?
        """, (room_number, computer_name))
        return cursor.fetchone()


# ---------------- Лицензии по ПК и аудитории ---------------- #

def get_licenses_for_computer(room_number, computer_name):
    """Возвращает все лицензии для конкретного ПК в аудитории."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT l.id, l.software, l.license_start, l.license_end, l.budget
            FROM licenses l
            JOIN computers c ON l.computer_id = c.id
            WHERE c.room_number = ? AND c.computer_name = ?
        """, (room_number, computer_name))
        return cursor.fetchall()


def get_licenses_for_room(room_number):
    """Возвращает все лицензии со всех компьютеров в аудитории."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.computer_name, l.software, l.license_start, l.license_end, l.budget
            FROM licenses l
            JOIN computers c ON l.computer_id = c.id
            WHERE c.room_number = ?
        """, (room_number,))
        return cursor.fetchall()


# ---------------- Все аудитории ---------------- #

def get_all_rooms():
    """Возвращает список всех аудиторий (уникальные номера)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT room_number FROM computers ORDER BY room_number")
        return [row[0] for row in cursor.fetchall()]


# ---------------- Добавление лицензии (по аудитории и ПК) ---------------- #

def add_license_by_room(room_number, computer_name, software, license_start, license_end, budget):
    """Добавляет лицензию через аудиторию и ПК (без ручного выбора computer_id)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        # Получаем id ПК
        cursor.execute("""
            SELECT id FROM computers WHERE room_number = ? AND computer_name = ?
        """, (room_number, computer_name))
        comp = cursor.fetchone()
        if not comp:
            raise ValueError("Компьютер не найден")
        comp_id = comp[0]

        cursor.execute("""
            INSERT INTO licenses (computer_id, software, license_start, license_end, budget)
            VALUES (?, ?, ?, ?, ?)
        """, (comp_id, software, license_start, license_end, budget))
        conn.commit()


# ---------------- Изменение лицензии (по аудитории, ПК и названию) ---------------- #

def update_license_by_details(room_number, computer_name, software, new_start, new_end):
    """
    Находит лицензию по аудитории, ПК и ПО, после чего обновляет даты.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT l.id FROM licenses l
            JOIN computers c ON l.computer_id = c.id
            WHERE c.room_number = ? AND c.computer_name = ? AND l.software = ?
        """, (room_number, computer_name, software))
        lic = cursor.fetchone()
        if not lic:
            raise ValueError("Лицензия не найдена")
        license_id = lic[0]

        cursor.execute("""
            UPDATE licenses SET license_start = ?, license_end = ? WHERE id = ?
        """, (new_start, new_end, license_id))
        conn.commit()


# ---------------- Пример ---------------- #
if __name__ == "__main__":
    init_db()

    # Добавим компьютер
    comp_id = add_computer("101", "PC-01")

    # Добавим лицензии
    add_license(comp_id, "MS Office 2021", "2025-01-01", "2026-01-01", 15000.0)
    add_license(comp_id, "AutoCAD 2024", "2025-02-01", "2026-02-01", 25000.0)

    # Получим все лицензии
    print("Все лицензии:", get_licenses())

    # Поиск
    print("Активные лицензии:", search_licenses(active_only=True))
