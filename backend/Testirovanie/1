from backend.db_functions import (
    add_data,
    delete_data,
    update_data,
    get_data,
    authorize_user
)


def test_add():
    try:
        add_data("users", ["test_user", "12345", "user"])
        print("Добавление работает")
    except Exception as e:
        print("Ошибка при добавлении:", e)


def test_get():
    try:
        data = get_data("users")
        print("Полученные данные:")
        print(data)
    except Exception as e:
        print("Ошибка при получении данных:", e)


def test_update():
    try:
        update_data(
            table="users",
            record_id=1,
            column="password",
            new_value="new_password"
        )
        print("Изменение работает")
    except Exception as e:
        print("Ошибка при изменении:", e)


def test_delete():
    try:
        delete_data("users", 1)
        print("Удаление работает")
    except Exception as e:
        print("Ошибка при удалении:", e)


def test_auth():
    try:
        result = authorize_user("admin", "admin123")

        if result:
            print("Авторизация работает")
            print(result)
        else:
            print("Неверный логин или пароль")

    except Exception as e:
        print("Ошибка при авторизации:", e)


if __name__ == "__main__":
    print("\n--- Проверка добавления ---")
    test_add()

    print("\n--- Проверка получения данных ---")
    test_get()

    print("\n--- Проверка изменения ---")
    test_update()

    print("\n--- Проверка авторизации ---")
    test_auth()

    print("\n--- Проверка удаления ---")
    test_delete()