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


def update_data(table, record_id, column, new_value):
    conn = get_connection()
    cursor = conn.cursor()

    query = f"UPDATE {table} SET {column} = %s WHERE id = %s"
    cursor.execute(query, (new_value, record_id))

    conn.commit()
    conn.close()


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

    cursor = None

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

    except Error as e:
        print(f"\nОшибка при выполнении SQL-запроса: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()   