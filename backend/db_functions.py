from database import get_connection
from pymysql import Error


# Разрешённые таблицы
ALLOWED_TABLES = {
    "users",
    "teachers",
    "event",
    "level",
    "type",
    "control",
    "teachers_events"
}


# Разрешённые колонки
ALLOWED_COLUMNS = {
    "users": {
        "id",
        "login",
        "password",
        "role"
    },

    "teachers": {
        "teacher_id",
        "name",
        "surname",
        "patronymic"
    },

    "event": {
        "event_id",
        "name",
        "place",
        "level",
        "event_date",
        "document",
        "type",
        "control",
        "description"
    },

    "level": {
        "level_id",
        "name"
    },

    "type": {
        "type_id",
        "name"
    },

    "control": {
        "control_id",
        "name"
    },

    "teachers_events": {
        "teacher",
        "event"
    }
}


# Первичные ключи
PRIMARY_KEYS = {
    "users": "id",
    "teachers": "teacher_id",
    "event": "event_id",
    "level": "level_id",
    "type": "type_id",
    "control": "control_id"
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

        query = f"""
            INSERT INTO {table}
            VALUES (NULL, {placeholders})
        """

        cursor.execute(query, values)
        conn.commit()

        return True

    except Error as e:
        print(f"Ошибка добавления данных: {e}")
        return False

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def delete_data(table, record_id):
    if table not in ALLOWED_TABLES:
        raise ValueError(f"Недопустимая таблица: {table}")

    if table not in PRIMARY_KEYS:
        raise ValueError(
            f"Для таблицы '{table}' не определён первичный ключ"
        )

    conn = None
    cursor = None

    try:
        conn = get_connection()

        if conn is None:
            return False

        cursor = conn.cursor()

        primary_key = PRIMARY_KEYS[table]

        query = f"""
            DELETE FROM {table}
            WHERE {primary_key} = %s
        """

        cursor.execute(query, (record_id,))
        conn.commit()

        return True

    except Error as e:
        print(f"Ошибка удаления данных: {e}")
        return False

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def update_data(table, record_id, column, new_value):
    if table not in ALLOWED_TABLES:
        raise ValueError(f"Недопустимая таблица: {table}")

    if table not in PRIMARY_KEYS:
        raise ValueError(
            f"Для таблицы '{table}' не определён первичный ключ"
        )

    if column not in ALLOWED_COLUMNS.get(table, set()):
        raise ValueError(
            f"Недопустимая колонка '{column}' для таблицы '{table}'"
        )

    conn = None
    cursor = None

    try:
        conn = get_connection()

        if conn is None:
            return False

        cursor = conn.cursor()

        primary_key = PRIMARY_KEYS[table]

        query = f"""
            UPDATE {table}
            SET {column} = %s
            WHERE {primary_key} = %s
        """

        cursor.execute(query, (new_value, record_id))
        conn.commit()

        return True

    except Error as e:
        print(f"Ошибка обновления данных: {e}")
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

        if columns is None:
            columns_sql = "*"
        else:
            allowed_columns = ALLOWED_COLUMNS.get(table, set())

            for column in columns:
                if column not in allowed_columns:
                    raise ValueError(
                        f"Недопустимая колонка '{column}' "
                        f"для таблицы '{table}'"
                    )

            columns_sql = ", ".join(columns)

        if record_id is not None:

            if table not in PRIMARY_KEYS:
                raise ValueError(
                    f"Для таблицы '{table}' "
                    f"не определён первичный ключ"
                )

            primary_key = PRIMARY_KEYS[table]

            query = f"""
                SELECT {columns_sql}
                FROM {table}
                WHERE {primary_key} = %s
            """

            cursor.execute(query, (record_id,))
            result = cursor.fetchone()

        else:
            query = f"""
                SELECT {columns_sql}
                FROM {table}
            """

            cursor.execute(query)
            result = cursor.fetchall()

        return result

    except Error as e:
        print(f"Ошибка получения данных: {e}")
        return None

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def authorize_user(login_input, password_input):
    conn = None
    cursor = None

    try:
        conn = get_connection()

        if conn is None:
            return None

        cursor = conn.cursor()

        query = """
            SELECT id, login, role
            FROM users
            WHERE login = %s
              AND password = %s
        """

        cursor.execute(
            query,
            (login_input, password_input)
        )

        user = cursor.fetchall()

        if user:
            print("\nУспешная авторизация!")
            print(
                f"Добро пожаловать! "
                f"ID: {user[0]['id']}, "
                f"Роль: {user[0]['role']}"
            )
            return user

        print("\nОшибка: неверный логин или пароль.")
        return None

    except Error as e:
        print(f"\nОшибка SQL: {e}")
        return None

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()