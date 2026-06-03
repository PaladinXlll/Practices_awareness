from database import get_connection
from pymysql import Error


def get_teacher_by_id(teacher_id):
    conn = get_connection()

    if conn is None:
        return None

    cursor = None

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT teacher_id,
                   surname,
                   name,
                   patronymic
            FROM teachers
            WHERE teacher_id = %s
        """, (teacher_id,))

        teacher = cursor.fetchone()

        if teacher is None:
            print("Преподаватель не найден")
            return None

        return teacher

    except Error as e:
        print(f"Ошибка при получении преподавателя: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        conn.close()


def add_teacher(surname, name, patronymic):
    conn = get_connection()

    if conn is None:
        return False

    cursor = None

    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO teachers (surname, name, patronymic)
            VALUES (%s, %s, %s)
        """, (surname, name, patronymic))

        conn.commit()
        print("Преподаватель добавлен")
        return True

    except Error as e:
        print(f"Ошибка при добавлении преподавателя: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        conn.close()


def update_teacher(teacher_id, surname, name, patronymic):
    conn = get_connection()

    if conn is None:
        return False

    cursor = None

    try:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE teachers
            SET surname = %s,
                name = %s,
                patronymic = %s
            WHERE teacher_id = %s
        """, (surname, name, patronymic, teacher_id))

        if cursor.rowcount == 0:
            print("Преподаватель не найден")
            return False

        conn.commit()
        print("Преподаватель обновлён")
        return True

    except Error as e:
        print(f"Ошибка при обновлении преподавателя: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        conn.close()


def delete_teacher(teacher_id):
    conn = get_connection()

    if conn is None:
        return False

    cursor = None

    try:
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM teachers
            WHERE teacher_id = %s
        """, (teacher_id,))

        if cursor.rowcount == 0:
            print("Преподаватель не найден")
            return False

        conn.commit()
        print("Преподаватель удалён")
        return True

    except Error as e:
        print(f"Ошибка при удалении преподавателя: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        conn.close()


def get_teachers():
    conn = get_connection()

    if conn is None:
        return []

    cursor = None

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT teacher_id,
                   surname,
                   name,
                   patronymic
            FROM teachers
            ORDER BY teacher_id
        """)

        return cursor.fetchall()

    except Error as e:
        print(f"Ошибка при получении списка преподавателей: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        conn.close()


def validate_teacher(surname, name, patronymic):
    if not surname.strip():
        return False, "Не заполнена фамилия"

    if not name.strip():
        return False, "Не заполнено имя"

    if not patronymic.strip():
        return False, "Не заполнено отчество"

    return True, ""

if __name__ == "__main__":
    print("Проверка get_teachers:")
    teachers = get_teachers()
    print(teachers)

    print("Проверка get_teacher_by_id:")
    teacher = get_teacher_by_id(3)
    print(teacher)
