from database import get_connection


def add_teacher(surname, name, patronymic):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO teachers (surname, name, patronymic)
        VALUES (?, ?, ?)
    """, (surname, name, patronymic))

    conn.commit()
    conn.close()


def update_teacher(teacher_id, surname, name, patronymic):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE teachers
        SET surname = ?,
            name = ?,
            patronymic = ?
        WHERE id = ?
    """, (surname, name, patronymic, teacher_id))

    conn.commit()
    conn.close()


def delete_teacher(teacher_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM teachers
        WHERE id = ?
    """, (teacher_id,))

    conn.commit()
    conn.close()


def get_teachers():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id,
               surname,
               name,
               patronymic
        FROM teachers
        ORDER BY surname, name
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

    return True, ""
