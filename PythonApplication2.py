import mysql.connector
from mysql.connector import Error

def authorize_user(db_config, login_input, password_input):

    "Функция для подключения к БД и проверки логина и пароля."

    try:
        connection = mysql.connector.connect(**db_config)
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            
            query = "SELECT id, login, role FROM users WHERE login = %s AND password = %s"
            
            cursor.execute(query, (login_input, password_input))
            
            user = cursor.fetchone()
            
            if user:
                print("\nУспешная авторизация!")
                print(f"Добро пожаловать! ID: {user['id']}, Роль: {user['role']}")
                return user
            else:
                print("\nОшибка: Неверный логин или пароль.")
                return None

    except Error as e:
        print(f"\n⚠️ Ошибка при работе с MySQL: {e}")
        return None
        
    finally:

        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_db_password',
    'database': 'your_database'
}

print("Попытка входа пользователя с логином '1111'")
authorize_user(db_config, login_input="1111", password_input="0000")

print("\nПопытка входа с несуществующими данными")
authorize_user(db_config, login_input="9999", password_input="1234")