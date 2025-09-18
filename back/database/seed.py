import random
from datetime import datetime, timedelta
from DB import init_db, get_connection
from Functions import add_user, add_computer, add_license


def random_date(start, end):
    """Генерирует случайную дату между start и end"""
    return start + timedelta(days=random.randint(0, (end - start).days))


def seed_users(n=20):
    for i in range(n):
        login = f"user{i+1}"
        password = f"pass{i+1}"
        add_user(login, password)


def seed_computers(n=20):
    ids = []
    for i in range(n):
        room = str(random.randint(100, 110))  # аудитории 100-110
        comp_name = f"PC-{i+1:02d}"
        comp_id = add_computer(room, comp_name)
        ids.append(comp_id)
    return ids


def seed_licenses(computer_ids, n=20):
    softwares = ["MS Office 2021", "AutoCAD 2024", "Photoshop 2024", "VS Code", "PyCharm Pro"]
    for i in range(n):
        comp_id = random.choice(computer_ids)
        software = random.choice(softwares)
        start = random_date(datetime(2024, 1, 1), datetime(2025, 1, 1))
        end = start + timedelta(days=365)  # лицензия на год
        budget = random.choice([None, random.randint(10000, 30000)])
        add_license(comp_id, software, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"), budget)


if __name__ == "__main__":
    init_db()
    seed_users(20)
    comps = seed_computers(20)
    seed_licenses(comps, 20)
    print("База успешно заполнена данными!")
