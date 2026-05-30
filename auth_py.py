from db_functions import authorize_user



if __name__ == "__main__":
    print("Попытка входа пользователя с логином '1111'")
    authorize_user(login_input="1111", password_input="0000")