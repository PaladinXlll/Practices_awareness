from database import get_connection #сдесь ссылка на бд
from pymysql import Error

def add_data(table, values):
    conn = get_connection()
    cursor = conn.cursor()

    placeholders = ", ".join(["?"] * len(values))
    query = f"INSERT INTO {table} VALUES (NULL, {placeholders})"

    cursor.execute(query, values)

    conn.commit()
    conn.close()

def delete_data(table, record_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = f"DELETE FROM {table} WHERE id = ?"
    cursor.execute(query, (record_id,))

    conn.commit()
    conn.close()


def update_data(table, record_id, column, new_value):
    conn = get_connection()
    cursor = conn.cursor()

    query = f"UPDATE {table} SET {column} = ? WHERE id = ?"
    cursor.execute(query, (new_value, record_id))

    conn.commit()
    conn.close()


def get_data(table, record_id=None, columns = ['*']):
    conn = get_connection()
    cursor = conn.cursor()

    if record_id is not None:
        query = f"SELECT {columns} FROM {table} WHERE id = ?"
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
