from db_functions import authorize_user


if __name__ == "__main__":
    login = input("Введите логин: ")
    password = input("Введите пароль: ")

    authorize_user(
        login_input=login,
        password_input=password
    )