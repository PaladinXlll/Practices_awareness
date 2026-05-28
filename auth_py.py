import mysql.connector
from mysql.connector import Error
from database import get_connection


def authorize_user(login_input, password_input):
    connection = get_connection()
    if not connection:
        return None

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT id, login, role FROM users WHERE login = %s AND password = %s"
        cursor.execute(query, (login_input, password_input))
        user = cursor.fetchone()

        if user:
            print("\n Успешная авторизация!")
            print(f"Добро пожаловать! ID: {user['id']}, Роль: {user['role']}")
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
        if connection and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    print("Попытка входа пользователя с логином '1111'")
    authorize_user(login_input="1111", password_input="0000")