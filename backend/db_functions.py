from backend.database import get_connection
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



ALLOWED_TABLES = {
    "users",
    "teachers",
    "event",
    "level",
    "type",
    "control",
    "teachers_events"
}


ALLOWED_COLUMNS = {
    "users": {"id", "login", "password", "role"},

    "teachers": {"teacher_id", "name", "surname", "patronymic"},

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

    "level": {"level_id", "name"},
    "type": {"type_id", "name"},
    "control": {"control_id", "name"},
    "teachers_events": {"teacher", "event"}
}


PRIMARY_KEYS = {
    "users": "id",
    "teachers": "teacher_id",
    "event": "event_id",
    "level": "level_id",
    "type": "type_id",
    "control": "control_id"
}


def check_sql_safety(table, columns=None):
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
    conn = None
    cursor = None

    try:
        conn = get_connection()

        if conn is None:
            return None

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

    except ValueError as e:
        print(f"Ошибка безопасности SQL: {e}")
        return None

    except Error as e:
        print(f"Ошибка SQL: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def execute_select(query, params=None, fetchone=False):
    return execute_query(
        query=query,
        params=params,
        fetchone=fetchone,
        fetchall=not fetchone
    )


def get_data(table, record_id=None, columns=None):
    try:
        check_sql_safety(table, columns)

        if columns:
            columns_sql = ", ".join(columns)
        else:
            columns_sql = "*"

        if record_id is not None:
            primary_key = get_primary_key(table)
            query = f"SELECT {columns_sql} FROM {table} WHERE {primary_key} = %s"
            return execute_query(query, (record_id,), fetchone=True)

        query = f"SELECT {columns_sql} FROM {table}"
        return execute_query(query, fetchall=True)

    except ValueError as e:
        print(f"Ошибка безопасности SQL: {e}")
        return None


def add_data(table, columns, values):
    check_sql_safety(table, columns)

    if len(columns) != len(values):
        raise ValueError("Количество колонок не совпадает с количеством значений")

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

    query = f"""
        DELETE FROM {table}
        WHERE {primary_key} = %s
    """

    return execute_query(query, (record_id,), commit=True)


def add_relation(table, first_column, second_column, first_id, second_id):
    check_sql_safety(table, [first_column, second_column])

    query = f"""
        INSERT INTO {table} ({first_column}, {second_column})
        VALUES (%s, %s)
    """

    return execute_query(query, (first_id, second_id), commit=True)


def delete_relation(table, first_column, second_column, first_id, second_id):
    check_sql_safety(table, [first_column, second_column])

    query = f"""
        DELETE FROM {table}
        WHERE {first_column} = %s AND {second_column} = %s
    """

    return execute_query(query, (first_id, second_id), commit=True)


def add_teacher_event(teacher_id, event_id):
    return add_relation(
        table="teachers_events",
        first_column="teacher",
        second_column="event",
        first_id=teacher_id,
        second_id=event_id
    )


def delete_teacher_event(teacher_id, event_id):
    return delete_relation(
        table="teachers_events",
        first_column="teacher",
        second_column="event",
        first_id=teacher_id,
        second_id=event_id
    )


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


