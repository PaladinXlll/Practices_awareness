from db_functions import add_teacher_event, delete_teacher_event, execute_select
from validators import validate_id


def add_teacher_to_event(teacher_id, event_id):
    is_valid, message = validate_id(teacher_id)

    if not is_valid:
        print(f"Некорректный ID преподавателя: {message}")
        return False

    is_valid, message = validate_id(event_id)

    if not is_valid:
        print(f"Некорректный ID мероприятия: {message}")
        return False

    result = add_teacher_event(teacher_id, event_id)

    if result:
        print("Преподаватель добавлен к мероприятию")
        return True

    print("Связь преподавателя и мероприятия не добавлена")
    return False


def remove_teacher_from_event(teacher_id, event_id):
    is_valid, message = validate_id(teacher_id)

    if not is_valid:
        print(f"Некорректный ID преподавателя: {message}")
        return False

    is_valid, message = validate_id(event_id)

    if not is_valid:
        print(f"Некорректный ID мероприятия: {message}")
        return False

    result = delete_teacher_event(teacher_id, event_id)

    if result == 0:
        print("Связь преподавателя и мероприятия не найдена")
        return False

    if result:
        print("Преподаватель удалён из мероприятия")
        return True

    print("Ошибка при удалении связи преподавателя и мероприятия")
    return False


def get_event_teachers(event_id):
    is_valid, message = validate_id(event_id)

    if not is_valid:
        print(f"Некорректный ID мероприятия: {message}")
        return None

    query = """
        SELECT
            teachers.teacher_id,
            teachers.surname,
            teachers.name,
            teachers.patronymic
        FROM teachers_events
        JOIN teachers
            ON teachers_events.teacher = teachers.teacher_id
        WHERE teachers_events.event = %s
    """

    return execute_select(query, (event_id,))


def get_teacher_events(teacher_id):
    is_valid, message = validate_id(teacher_id)

    if not is_valid:
        print(f"Некорректный ID преподавателя: {message}")
        return None

    query = """
        SELECT
            event.event_id,
            event.name,
            event.place,
            event.level,
            event.event_date,
            event.document,
            event.type,
            event.control,
            event.description
        FROM teachers_events
        JOIN event
            ON teachers_events.event = event.event_id
        WHERE teachers_events.teacher = %s
    """

    return execute_select(query, (teacher_id,))

