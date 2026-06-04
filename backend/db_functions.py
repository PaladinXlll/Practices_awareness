<<<<<<< HEAD
from database import get_connection
from pymysql import Error


ALLOWED_TABLES = {
    "users",
    "teachers",
    "events",
    "level",
    "type",
    "control",
    "teachers_events"
}
=======
from backend.database import get_connection
from pymysql import Error

print("ЗАГРУЖЕН НОВЫЙ db_functions.py")

def add_data(table, values):
    conn = get_connection()
    cursor = conn.cursor()

    placeholders = ", ".join(["%s"] * len(values))
    query = f"INSERT INTO {table} VALUES (NULL, {placeholders})"

    cursor.execute(query, values)

    conn.commit()
    conn.close()


def delete_data(table, record_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = f"DELETE FROM {table} WHERE id = %s"
    cursor.execute(query, (record_id,))

    conn.commit()
    conn.close()
>>>>>>> fe7927ad128842b6d761d5ba13dd53c77f5d96ac


ALLOWED_COLUMNS = {
    "users": {"id", "login", "password", "role"},

<<<<<<< HEAD
    "teachers": {"teacher_id", "name", "surname", "patronymic"},
=======
    query = f"UPDATE {table} SET {column} = %s WHERE id = %s"
    cursor.execute(query, (new_value, record_id))
>>>>>>> fe7927ad128842b6d761d5ba13dd53c77f5d96ac

    "events": {
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

    "level": {"level_id", "name"},
    "type": {"type_id", "name"},
    "control": {"control_id", "name"},
    "teachers_events": {"teacher", "event"}
}


<<<<<<< HEAD
PRIMARY_KEYS = {
    "users": "id",
    "teachers": "teacher_id",
    "events": "event_id",
    "level": "level_id",
    "type": "type_id",
    "control": "control_id"
}
=======
def get_data(table, record_id=None, columns=["*"]):
    conn = get_connection()
    cursor = conn.cursor()

    columns_str = ", ".join(columns)

    if record_id is not None:
        query = f"SELECT {columns_str} FROM {table} WHERE id = %s"
        cursor.execute(query, (record_id,))
        result = cursor.fetchone()
    else:
        query = f"SELECT {columns_str} FROM {table}"
        cursor.execute(query)
        result = cursor.fetchall()

    conn.close()
    return result


def authorize_user(login_input, password_input):
    connection = get_connection()
    if not connection:
        return None
>>>>>>> fe7927ad128842b6d761d5ba13dd53c77f5d96ac


def check_sql_safety(table, columns=None):
    """
    Первая защита от SQL-инъекций:
    проверяем, что таблица и колонки есть в белом списке.
    """

    if table not in ALLOWED_TABLES:
        raise ValueError(f"Недопустимая таблица: {table}")

    if columns is not None:
        allowed_columns = ALLOWED_COLUMNS.get(table, set())

        for column in columns:
            if column not in allowed_columns:
                raise ValueError(f"Недопустимая колонка: {column}")

    return True


def get_primary_key(table):
    check_sql_safety(table)

    primary_key = PRIMARY_KEYS.get(table)

    if primary_key is None:
        raise ValueError(f"Для таблицы {table} не указан primary key")

    return primary_key


def execute_query(query, params=None, fetchone=False, fetchall=False, commit=False):
    """
    Вторая защита от SQL-инъекций:
    значения передаются отдельно через params, а не вставляются в SQL строку.
    """

    conn = None
    cursor = None
<<<<<<< HEAD

    try:
        conn = get_connection()

        if conn is None:
            return None
=======

    try:
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
                f"Добро пожаловать! ID: {user[0]['id']}, "
                f"Роль: {user[0]['role']}"
            )
            return user

        print("\nОшибка: Неверный логин или пароль.")
        return None
>>>>>>> fe7927ad128842b6d761d5ba13dd53c77f5d96ac

        cursor = conn.cursor()

        if params is None:
            params = ()

        cursor.execute(query, params)

        result = None

        if fetchone:
            result = cursor.fetchone()

        if fetchall:
            result = cursor.fetchall()

        if commit:
            conn.commit()
            result = cursor.rowcount

        return result

    except Error as e:
<<<<<<< HEAD
        print(f"Ошибка SQL: {e}")
=======
        print(f"\nОшибка при выполнении SQL-запроса: {e}")
>>>>>>> fe7927ad128842b6d761d5ba13dd53c77f5d96ac
        return None

    finally:
        if cursor:
            cursor.close()
<<<<<<< HEAD
        if conn:
            conn.close()


def get_data(table, record_id=None, columns=None):
    check_sql_safety(table, columns)

    primary_key = get_primary_key(table)

    if columns:
        columns_sql = ", ".join(columns)
    else:
        columns_sql = "*"

    if record_id is not None:
        query = f"SELECT {columns_sql} FROM {table} WHERE {primary_key} = %s"
        return execute_query(query, (record_id,), fetchone=True)

    query = f"SELECT {columns_sql} FROM {table}"
    return execute_query(query, fetchall=True)


def add_data(table, columns, values):
    check_sql_safety(table, columns)

    columns_sql = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(values))

    query = f"""
        INSERT INTO {table} ({columns_sql})
        VALUES ({placeholders})
    """

    return execute_query(query, values, commit=True)


def update_data(table, record_id, update_values):
    columns = list(update_values.keys())

    check_sql_safety(table, columns)

    primary_key = get_primary_key(table)

    set_sql = ", ".join([f"{column} = %s" for column in columns])
    values = list(update_values.values())
    values.append(record_id)

    query = f"""
        UPDATE {table}
        SET {set_sql}
        WHERE {primary_key} = %s
    """

    return execute_query(query, values, commit=True)


def delete_data(table, record_id):
    check_sql_safety(table)

    primary_key = get_primary_key(table)

    query = f"DELETE FROM {table} WHERE {primary_key} = %s"

    return execute_query(query, (record_id,), commit=True)


def authorize_user(login_input, password_input):
    query = """
        SELECT id, login, role
        FROM users
        WHERE login = %s AND password = %s
    """

    user = execute_query(
        query,
        (login_input, password_input),
        fetchone=True
    )

    if user:
        print("\nУспешная авторизация!")
        print(f"Добро пожаловать! ID: {user['id']}, Роль: {user['role']}")
        return user

    print("\nОшибка: Неверный логин или пароль.")
    return None
=======
        if connection:
            connection.close()   
>>>>>>> fe7927ad128842b6d761d5ba13dd53c77f5d96ac
