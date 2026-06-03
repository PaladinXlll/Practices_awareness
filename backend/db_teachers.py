from db_functions import get_data, add_data, update_data, delete_data


def get_teachers():
    return get_data(
        table="teachers",
        columns=["teacher_id", "surname", "name", "patronymic"]
    )


def get_teacher_by_id(teacher_id):
    return get_data(
        table="teachers",
        record_id=teacher_id,
        columns=["teacher_id", "surname", "name", "patronymic"]
    )


def add_teacher(surname, name, patronymic):
    result = add_data(
        table="teachers",
        columns=["surname", "name", "patronymic"],
        values=(surname, name, patronymic)
    )

    if result:
        print("Преподаватель добавлен")
        return True

    print("Преподаватель не добавлен")
    return False


def update_teacher(teacher_id, surname, name, patronymic):
    result = update_data(
        table="teachers",
        record_id=teacher_id,
        update_values={
            "surname": surname,
            "name": name,
            "patronymic": patronymic
        }
    )

    if result == 0:
        print("Преподаватель не найден")
        return False

    if result:
        print("Преподаватель обновлён")
        return True

    print("Ошибка при обновлении преподавателя")
    return False


def delete_teacher(teacher_id):
    result = delete_data(
        table="teachers",
        record_id=teacher_id
    )

    if result == 0:
        print("Преподаватель не найден")
        return False

    if result:
        print("Преподаватель удалён")
        return True

    print("Ошибка при удалении преподавателя")
    return False


def validate_teacher(surname, name, patronymic):
    if not surname.strip():
        return False, "Не заполнена фамилия"

    if not name.strip():
        return False, "Не заполнено имя"

    if not patronymic.strip():
        return False, "Не заполнено отчество"

    return True, ""
