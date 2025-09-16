import sqlite3

DB_NAME = "university.db"


def get_connection():
    """Создаёт подключение к базе данных."""
    return sqlite3.connect(DB_NAME)


def init_db():
    """Создаёт таблицы, если их ещё нет."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Пользователи
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            last_login DATETIME
        )
        """)

        # Компьютеры
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS computers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_number TEXT NOT NULL,
            computer_name TEXT NOT NULL
        )
        """)

        # Лицензии
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS licenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            computer_id INTEGER NOT NULL,
            software TEXT NOT NULL,
            license_start DATE NOT NULL,
            license_end DATE NOT NULL,
            budget REAL,
            FOREIGN KEY (computer_id) REFERENCES computers (id) ON DELETE CASCADE
        )
        """)

        conn.commit()


if __name__ == "__main__":
    init_db()
    print("База данных успешно инициализирована ✅")
