import pymysql
from pymysql import Error
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE=os.getenv("DATABASE")
USER=os.getenv("LOGIN")
PASSWORD=os.getenv("PASSWORD")

db_config = {
    'host': '192.168.200.18',
    'port': 3306,
    'user': USER,
    'password': PASSWORD,
    'database': DATABASE,
    'ssl_disabled': True,
    'cursorclass': 'pymysql.cursors.DictCursor'
}

def get_connection():
    try:
        connection = pymysql.connect(**db_config)
        print('Подключено')
        return connection
    except Error as e:
        print(f"️ Ошибка подключения к MySQL: {e}")
        return None