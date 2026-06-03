from database import get_connection  # ссылка на БД
from pymysql import Error

# Разрешённые таблицы
ALLOWED_TABLES = {
    "users",
    "products",
    "orders"
}

# Разрешённые колонки для каждой таблицы
ALLOWED_COLUMNS = {
    "users": {"id", "login", "password", "role"},
    "products": {"id", "name", "price"},
    "orders": {"id", "status"}
}


def add_data(table, values):
    if table not in ALLOWED_TABLES:
        raise ValueError(f"Недопустимая таблица: {table}")

    conn = None
    cursor = None

    try:
        conn = get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()

        placeholders = ", ".join(["%s"] * len(values))
        query = f"INSERT INTO {table} VALUES (NULL, {placeholders})"

        cursor.execute(query, values)
        conn.commit()

        return True

    except Error as e:
        print(f"Ошибка SQL при добавлении данных: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def delete_data(table, record_id):
    if table not in ALLOWED_TABLES:
        raise ValueError(f"Недопустимая таблица: {table}")

    conn = None
    cursor = None

    try:
        conn = get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()

        query = f"DELETE FROM {table} WHERE id = %s"
        cursor.execute(query, (record_id,))

        conn.commit()

        return True

    except Error as e:
        print(f"Ошибка SQL при удалении данных: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def update_data(table, record_id, column, new_value):
    if table not in ALLOWED_TABLES:
        raise ValueError(f"Недопустимая таблица: {table}")

    if column not in ALLOWED_COLUMNS.get(table, set()):
        raise ValueError(f"Недопустимая колонка: {column}")

    conn = None
    cursor = None

    try:
        conn = get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()

        query = f"UPDATE {table} SET {column} = %s WHERE id = %s"

        cursor.execute(query, (new_value, record_id))
        conn.commit()

        return True

    except Error as e:
        print(f"Ошибка SQL при обновлении данных: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_data(table, record_id=None, columns=None):
    if table not in ALLOWED_TABLES:
        raise ValueError(f"Недопустимая таблица: {table}")

    conn = None
    cursor = None

    try:
        conn = get_connection()
        if conn is None:
            return None

        cursor = conn.cursor()

        if columns:
            allowed_columns = ALLOWED_COLUMNS.get(table, set())

            for col in columns:
                if col not in allowed_columns:
                    raise ValueError(f"Недопустимая колонка: {col}")

            columns_sql = ", ".join(columns)
        else:
            columns_sql = "*"

        if record_id is not None:
            query = f"SELECT {columns_sql} FROM {table} WHERE id = %s"
            cursor.execute(query, (record_id,))
            result = cursor.fetchone()
        else:
            query = f"SELECT {columns_sql} FROM {table}"
            cursor.execute(query)
            result = cursor.fetchall()

        return result

    except Error as e:
        print(f"Ошибка SQL при получении данных: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def authorize_user(login_input, password_input):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        if not connection:
            return None

        cursor = connection.cursor()

        query = """
            SELECT id, login, role
            FROM users
            WHERE login = %s AND password = %s
        """

        cursor.execute(query, (login_input, password_input))
        user = cursor.fetchall()

        if user:
            print("\nУспешная авторизация!")
            print(
                f"Добро пожаловать! "
                f"ID: {user[0]['id']}, "
                f"Роль: {user[0]['role']}"
            )
            return user

        print("\nОшибка: Неверный логин или пароль.")
        return None

    except Error as e:
        print(f"\nОшибка при выполнении SQL-запроса: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()