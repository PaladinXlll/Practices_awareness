from .db_functions import get_data, add_data, update_data, delete_data
from .validators import validate_teacher_data, validate_id

TEACHER_COLUMNS = ["teacher_id", "surname", "name", "patronymic"]


def get_teachers():
    return get_data(
        table="teachers",
        columns=TEACHER_COLUMNS
    )


def get_teacher_by_id(teacher_id):
    is_valid, message = validate_id(teacher_id)

    if not is_valid:
        print(message)
        return None

    return get_data(
        table="teachers",
        record_id=teacher_id,
        columns=TEACHER_COLUMNS
    )


def add_teacher(surname, name, patronymic):
    is_valid, message = validate_teacher_data(surname, name, patronymic)

    if not is_valid:
        print(message)
        return False

    result = add_data(
        table="teachers",
        columns=["surname", "name", "patronymic"],
        values=(surname.strip(), name.strip(), patronymic.strip())
    )

    if result:
        print("Преподаватель добавлен")
        return True

    print("Преподаватель не добавлен")
    return False


def update_teacher(teacher_id, surname, name, patronymic):
    is_valid, message = validate_id(teacher_id)

    if not is_valid:
        print(message)
        return False

    is_valid, message = validate_teacher_data(surname, name, patronymic)

    if not is_valid:
        print(message)
        return False

    result = update_data(
        table="teachers",
        record_id=teacher_id,
        update_values={
            "surname": surname.strip(),
            "name": name.strip(),
            "patronymic": patronymic.strip()
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
    is_valid, message = validate_id(teacher_id)

    if not is_valid:
        print(message)
        return False

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

