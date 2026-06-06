from backend.db_functions import (
    add_data,
    get_data,
    update_data,
    delete_data,
    authorize_user
)


def test_add():
    print("\n[1] Добавление пользователя")

    result = add_data(
        "users",
        ["login", "password", "role"],
        ["test_user", "12345", "user"]
    )

    print("Результат:", result)


def test_get():
    print("\n[2] Получение пользователей")

    users = get_data("users")

    if users:
        print("Количество записей:", len(users))

        for user in users:
            print(user)
    else:
        print("Данные не найдены")


def test_update():
    print("\n[3] Изменение пользователя")

    users = get_data("users")

    if not users:
        print("Нет данных для изменения")
        return

    user_id = users[-1]["id"]

    result = update_data(
        "users",
        user_id,
        {
            "password": "99999"
        }
    )

    print("Изменено строк:", result)


def test_auth():
    print("\n[4] Авторизация")

    user = authorize_user(
        "test_user",
        "99999"
    )

    if user:
        print("Авторизация успешна")
    else:
        print("Авторизация не прошла")


def test_delete():
    print("\n[5] Удаление пользователя")

    users = get_data("users")

    if not users:
        print("Нет записей для удаления")
        return

    user_id = users[-1]["id"]

    result = delete_data(
        "users",
        user_id
    )

    print("Удалено строк:", result)


if __name__ == "__main__":
    print("=== Проверка функций БД ===")

    test_add()
    test_get()
    test_update()
    test_auth()
    test_delete()

    print("\n=== Проверка закончена ===")