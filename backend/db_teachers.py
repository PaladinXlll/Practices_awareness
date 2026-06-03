from database import get_connection


def add_teacher(surname, name, patronymic):
    conn = get_connection()

    if conn is None:
        return None

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO teachers (surname, name, patronymic)
        VALUES (%s, %s, %s)
    """, (surname, name, patronymic))

    conn.commit()
    conn.close()

    print("Преподаватель добавлен")


def update_teacher(teacher_id, surname, name, patronymic):
    conn = get_connection()

    if conn is None:
        return None

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE teachers
        SET surname = %s,
            name = %s,
            patronymic = %s
        WHERE teacher_id = %s
    """, (surname, name, patronymic, teacher_id))

    if cursor.rowcount == 0:
        print("Преподаватель с таким ID не найден")
    else:
        print("Данные преподавателя обновлены")

    conn.commit()
    conn.close()


def delete_teacher(teacher_id):
    conn = get_connection()

    if conn is None:
        return None

    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM teachers
        WHERE teacher_id = %s
    """, (teacher_id,))

    if cursor.rowcount == 0:
        print("Преподаватель с таким ID не найден")
    else:
        print("Преподаватель удалён")

    conn.commit()
    conn.close()


def get_teachers():
    conn = get_connection()

    if conn is None:
        return None

    cursor = conn.cursor()

    cursor.execute("""
        SELECT teacher_id,
               surname,
               name,
               patronymic
        FROM teachers
        ORDER BY teacher_id
    """)

    teachers = cursor.fetchall()

    conn.close()

    return teachers


def validate_teacher(surname, name, patronymic):
    if not surname.strip():
        return False, "Не заполнена фамилия"

    if not name.strip():
        return False, "Не заполнено имя"

    if not patronymic.strip():
        return False, "Не заполнено отчество"

    return True, "Все данные заполнены"


if __name__ == "__main__":
    print(get_teachers())
