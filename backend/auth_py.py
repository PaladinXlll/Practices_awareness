from db_functions import authorize_user

def main():

    login = input("Введите логин: ").strip()

    password = input("Введите пароль: ").strip()

    authorize_user(

        login_input=login,

        password_input=password

    )

