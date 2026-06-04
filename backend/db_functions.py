from database import get_connection  # сдесь ссылка на бд
from pymysql import Error


def validate_teacher_id(teacher_id):
    """Проверка, что teacher_id число и > 0"""
    if not isinstance(teacher_id, (int, float)) or isinstance(teacher_id, bool):
        return False, "teacher_id должен быть числом"
    if teacher_id <= 0:
        return False, "teacher_id должен быть больше 0"
    return True, ""


def check_teacher_exists(cursor, teacher_id):
    """Проверка существования преподавателя"""
    cursor.execute("SELECT id FROM teachers WHERE id = %s", (teacher_id,))
    return cursor.fetchone() is not None


def add_data(table, values):
    conn = get_connection()
    if conn is None:
        return None
    cursor = conn.cursor()

    placeholders = ", ".join(["%s"] * len(values))
    query = f"INSERT INTO {table} VALUES (NULL, {placeholders})"

    cursor.execute(query, values)

    conn.commit()
    conn.close()


def delete_data(table, record_id):
    conn = get_connection()
    if conn is None:
        return None
    cursor = conn.cursor()

    # Добавлено: проверка для teachers
    if table == "teachers":
        is_valid, msg = validate_teacher_id(record_id)
        if not is_valid:
            print(msg)
            conn.close()
            return None
        if not check_teacher_exists(cursor, record_id):
            print("Преподаватель не найден")
            conn.close()
            return None

    query = f"DELETE FROM {table} WHERE id = %s"
    cursor.execute(query, (record_id,))

    conn.commit()
    conn.close()

    # Добавлено: сообщение
    if table == "teachers":
        print("Преподаватель удалён")


def update_data(table, record_id, column, new_value):
    conn = get_connection()
    if conn is None:
        return None
    cursor = conn.cursor()

    # Добавлено: проверка для teachers
    if table == "teachers":
        is_valid, msg = validate_teacher_id(record_id)
        if not is_valid:
            print(msg)
            conn.close()
            return None
        if not check_teacher_exists(cursor, record_id):
            print("Преподаватель не найден")
            conn.close()
            return None

    query = f"UPDATE {table} SET {column} = %s WHERE id = %s"
    cursor.execute(query, (new_value, record_id))

    conn.commit()
    conn.close()

    # Добавлено: сообщение
    if table == "teachers":
        print("Данные обновлены")


def get_data(table, record_id=None, columns=['*']):
    conn = get_connection()
    if conn is None:
        return None
    cursor = conn.cursor()

    # Добавлено: проверка для teachers
    if table == "teachers" and record_id is not None:
        is_valid, msg = validate_teacher_id(record_id)
        if not is_valid:
            print(msg)
            conn.close()
            return None
        if not check_teacher_exists(cursor, record_id):
            print("Преподаватель не найден")
            conn.close()
            return None

    columns = ", ".join(columns)
    if record_id is not None:
        query = f"SELECT {columns} FROM {table} WHERE id = %s"
        cursor.execute(query, (record_id,))
        result = cursor.fetchone()
    else:
        query = f"SELECT {columns} FROM {table}"
        cursor.execute(query)
        result = cursor.fetchall()

    conn.close()
    return result


def authorize_user(login_input, password_input):
    connection = get_connection()
    if not connection:
        return None

    cursor = None
    try:
        cursor = connection.cursor()
        query = "SELECT id, login, role FROM users WHERE login = %s AND password = %s"
        cursor.execute(query, (login_input, password_input))
        user = cursor.fetchall()

        if user:
            print("\n Успешная авторизация!")
            print(f"Добро пожаловать! ID: {user[0]['id']}, Роль: {user[0]['role']}")
            return user
        else:
            print("\n Ошибка: Неверный логин или пароль.")
            return None

    except Error as e:
        print(f"\n Ошибка при выполнении SQL-запроса: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()