from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from datetime import datetime
import sys
import os
import logging
import json

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Добавляем путь к папке database для импорта
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'database'))

from database.Functions import (
    add_user, authenticate_user, get_users,
    add_computer, get_computers, delete_computer,
    add_license, get_licenses, update_license, delete_license, search_licenses
)
from database.DB import init_db

app = Flask(__name__)
CORS(app)  # Разрешаем CORS для фронтенда
app.config['JSON_AS_ASCII'] = False

# Инициализируем базу данных при запуске
init_db()

# ==================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==================== #

def validate_required_fields(data, required_fields):
    """Проверяет наличие обязательных полей в данных"""
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    if missing_fields:
        return False, f"Отсутствуют обязательные поля: {', '.join(missing_fields)}"
    return True, None

def validate_date_format(date_string):
    """Проверяет формат даты YYYY-MM-DD"""
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def success_response(data=None, message="Успешно"):
    """Стандартный успешный ответ"""
    response = {"success": True, "message": message}
    if data is not None:
        response["data"] = data
    return Response(
        json.dumps(response, ensure_ascii=False),
        content_type="application/json; charset=utf-8"
    )

def error_response(message, status_code=400):
    """Стандартный ответ с ошибкой"""
    response = {"success": False, "error": message}
    return Response(
        json.dumps(response, ensure_ascii=False),
        content_type="application/json; charset=utf-8"
    ), status_code


# ==================== АУТЕНТИФИКАЦИЯ ==================== #

@app.route('/auth/register', methods=['POST'])
def register():
    """Регистрация нового пользователя"""
    try:
        logger.info("=== REGISTER REQUEST ===")
        logger.info(f"Content-Type: {request.content_type}")
        logger.info(f"Raw data: {request.data}")
        
        data = request.get_json()
        logger.info(f"Parsed JSON: {data}")
        
        # Проверяем что данные переданы
        if not data:
            logger.error("ERROR: No JSON data received")
            return error_response("Не переданы данные в формате JSON")
        
        # Валидация входных данных
        is_valid, error_msg = validate_required_fields(data, ['login', 'password'])
        if not is_valid:
            return error_response(error_msg)
        
        login = data['login'].strip()
        password = data['password']
        
        # Проверка минимальной длины
        if len(login) < 3:
            return error_response("Логин должен содержать минимум 3 символа")
        if len(password) < 4:
            return error_response("Пароль должен содержать минимум 4 символа")
        
        # Добавляем пользователя
        add_user(login, password)
        return success_response(message="Пользователь успешно зарегистрирован")
        
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            return error_response("Пользователь с таким логином уже существует")
        return error_response(f"Ошибка при регистрации: {str(e)}", 500)

@app.route('/auth/login', methods=['POST'])
def login():
    """Аутентификация пользователя"""
    try:
        data = request.get_json()
        
        # Проверяем что данные переданы
        if not data:
            return error_response("Не переданы данные в формате JSON")
        
        # Валидация входных данных
        is_valid, error_msg = validate_required_fields(data, ['login', 'password'])
        if not is_valid:
            return error_response(error_msg)
        
        login = data['login'].strip()
        password = data['password']
        
        # Проверяем аутентификацию
        if authenticate_user(login, password):
            return success_response({"login": login}, "Успешная аутентификация")
        else:
            return error_response("Неверный логин или пароль", 401)
            
    except Exception as e:
        return error_response(f"Ошибка при аутентификации: {str(e)}", 500)

# ==================== ПОЛЬЗОВАТЕЛИ ==================== #

@app.route('/users', methods=['GET'])
def get_all_users():
    """Получить всех пользователей"""
    try:
        users = get_users()
        users_list = []
        for user in users:
            users_list.append({
                'id': user[0],
                'login': user[1],
                'last_login': user[2]
            })
        return success_response(users_list)
    except Exception as e:
        return error_response(f"Ошибка при получении пользователей: {str(e)}", 500)

@app.route('/users', methods=['POST'])
def create_user():
    """Создать нового пользователя (то же что и регистрация)"""
    return register()

# ==================== КОМПЬЮТЕРЫ ==================== #

@app.route('/computers', methods=['GET'])
def get_all_computers():
    """Получить все компьютеры"""
    try:
        computers = get_computers()
        computers_list = []
        for computer in computers:
            computers_list.append({
                'id': computer[0],
                'room_number': computer[1],
                'computer_name': computer[2]
            })
        return success_response(computers_list)
    except Exception as e:
        return error_response(f"Ошибка при получении компьютеров: {str(e)}", 500)

@app.route('/computers', methods=['POST'])
def create_computer():
    """Добавить новый компьютер"""
    try:
        data = request.get_json()
        
        # Валидация входных данных
        is_valid, error_msg = validate_required_fields(data, ['room_number', 'computer_name'])
        if not is_valid:
            return error_response(error_msg)
        
        room_number = data['room_number'].strip()
        computer_name = data['computer_name'].strip()
        
        # Добавляем компьютер
        computer_id = add_computer(room_number, computer_name)
        return success_response({"id": computer_id}, "Компьютер успешно добавлен")
        
    except Exception as e:
        return error_response(f"Ошибка при добавлении компьютера: {str(e)}", 500)

@app.route('/computers/<int:computer_id>', methods=['DELETE'])
def delete_computer_by_id(computer_id):
    """Удалить компьютер"""
    try:
        delete_computer(computer_id)
        return success_response(message="Компьютер успешно удален")
    except Exception as e:
        return error_response(f"Ошибка при удалении компьютера: {str(e)}", 500)

# ==================== ЛИЦЕНЗИИ ==================== #

@app.route('/licenses', methods=['GET'])
def get_all_licenses():
    """Получить все лицензии"""
    try:
        computer_id = request.args.get('computer_id')
        if computer_id:
            licenses = get_licenses(int(computer_id))
        else:
            licenses = get_licenses()
            
        licenses_list = []
        for license_item in licenses:
            licenses_list.append({
                'id': license_item[0],
                'computer_id': license_item[1],
                'software': license_item[2],
                'license_start': license_item[3],
                'license_end': license_item[4],
                'budget': license_item[5]
            })
        return success_response(licenses_list)
    except Exception as e:
        return error_response(f"Ошибка при получении лицензий: {str(e)}", 500)

@app.route('/licenses', methods=['POST'])
def create_license():
    """Добавить новую лицензию"""
    try:
        data = request.get_json()
        
        # Валидация входных данных
        is_valid, error_msg = validate_required_fields(data, ['computer_id', 'software', 'license_start', 'license_end'])
        if not is_valid:
            return error_response(error_msg)
        
        computer_id = data['computer_id']
        software = data['software'].strip()
        license_start = data['license_start']
        license_end = data['license_end']
        budget = data.get('budget', 0.0)
        
        # Проверка существования компьютера
        computers = get_computers()
        computer_exists = any(computer[0] == computer_id for computer in computers)
        if not computer_exists:
            return error_response(f"Компьютер с ID {computer_id} не найден")
        
        # Валидация дат
        if not validate_date_format(license_start):
            return error_response("Неверный формат даты начала лицензии (требуется YYYY-MM-DD)")
        if not validate_date_format(license_end):
            return error_response("Неверный формат даты окончания лицензии (требуется YYYY-MM-DD)")
        
        # Проверка что дата окончания больше даты начала
        start_date = datetime.strptime(license_start, '%Y-%m-%d')
        end_date = datetime.strptime(license_end, '%Y-%m-%d')
        if end_date <= start_date:
            return error_response("Дата окончания лицензии должна быть больше даты начала")
        
        # Добавляем лицензию
        add_license(computer_id, software, license_start, license_end, budget)
        return success_response(message="Лицензия успешно добавлена")
        
    except Exception as e:
        return error_response(f"Ошибка при добавлении лицензии: {str(e)}", 500)

@app.route('/licenses/<int:license_id>', methods=['PUT'])
def update_license_by_id(license_id):
    """Обновить лицензию"""
    try:
        data = request.get_json()
        if not data:
            return error_response("Не переданы данные для обновления")
        
        # Валидация дат если они переданы
        if 'license_start' in data and not validate_date_format(data['license_start']):
            return error_response("Неверный формат даты начала лицензии (требуется YYYY-MM-DD)")
        if 'license_end' in data and not validate_date_format(data['license_end']):
            return error_response("Неверный формат даты окончания лицензии (требуется YYYY-MM-DD)")
        
        # Очистка строковых полей от пробелов
        if 'software' in data:
            data['software'] = data['software'].strip()
        
        # Обновляем лицензию
        update_license(license_id, **data)
        return success_response(message="Лицензия успешно обновлена")
        
    except Exception as e:
        return error_response(f"Ошибка при обновлении лицензии: {str(e)}", 500)

@app.route('/licenses/<int:license_id>', methods=['DELETE'])
def delete_license_by_id(license_id):
    """Удалить лицензию"""
    try:
        delete_license(license_id)
        return success_response(message="Лицензия успешно удалена")
    except Exception as e:
        return error_response(f"Ошибка при удалении лицензии: {str(e)}", 500)

@app.route('/licenses/search', methods=['GET'])
def search_licenses_endpoint():
    """Поиск лицензий с фильтрацией"""
    try:
        software = request.args.get('software')
        room = request.args.get('room')
        active_only = request.args.get('active_only', 'false').lower() == 'true'
        
        licenses = search_licenses(software=software, room=room, active_only=active_only)
        
        licenses_list = []
        for license_item in licenses:
            licenses_list.append({
                'id': license_item[0],
                'room_number': license_item[1],
                'computer_name': license_item[2],
                'software': license_item[3],
                'license_start': license_item[4],
                'license_end': license_item[5],
                'budget': license_item[6]
            })
        return success_response(licenses_list)
    except Exception as e:
        return error_response(f"Ошибка при поиске лицензий: {str(e)}", 500)

# ==================== ГЛАВНАЯ СТРАНИЦА ==================== #

@app.route('/', methods=['GET'])
def home():
    """Главная страница API"""
    return success_response({
        "message": "License Manager API",
        "version": "1.0",
        "endpoints": {
            "auth": ["/auth/login", "/auth/register"],
            "users": ["/users"],
            "computers": ["/computers"],
            "licenses": ["/licenses", "/licenses/search"]
        }
    })

# ==================== ОБРАБОТКА ОШИБОК ==================== #

@app.errorhandler(404)
def not_found(error):
    return error_response("Эндпоинт не найден", 404)

@app.errorhandler(405)
def method_not_allowed(error):
    return error_response("Метод не разрешен", 405)

@app.errorhandler(500)
def internal_error(error):
    return error_response("Внутренняя ошибка сервера", 500)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
