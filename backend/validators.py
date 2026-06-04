from datetime import datetime


def validate_id(value):
    try:
        value = int(value)
    except (TypeError, ValueError):
        return False, "ID должен быть числом"

    if value <= 0:
        return False, "ID должен быть больше 0"

    return True, ""


def validate_name_field(value, field_name):
    if value is None:
        return False, f"{field_name} не заполнено"

    value = value.strip()

    if not value:
        return False, f"{field_name} не заполнено"

    if len(value) < 2:
        return False, f"{field_name} должно содержать минимум 2 символа"

    if len(value) > 32:
        return False, f"{field_name} должно содержать максимум 32 символа"

    for char in value:
        if not (char.isalpha() or char == " " or char == "-"):
            return False, f"{field_name} содержит недопустимые символы"

    return True, ""


def validate_teacher_data(surname, name, patronymic):
    checks = [
        validate_name_field(surname, "Фамилия"),
        validate_name_field(name, "Имя"),
        validate_name_field(patronymic, "Отчество")
    ]

    for is_valid, message in checks:
        if not is_valid:
            return False, message

    return True, ""


def validate_date(value):
    if value is None:
        return False, "Дата не заполнена"

    value = str(value).strip()

    if not value:
        return False, "Дата не заполнена"

    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False, "Дата должна быть в формате YYYY-MM-DD"

    return True, ""


def validate_event_data(name, place, level, event_date, document, event_type, control, description):
    if name is None or not str(name).strip():
        return False, "Название мероприятия не заполнено"

    if len(str(name).strip()) > 256:
        return False, "Название мероприятия слишком длинное"

    if place is None or not str(place).strip():
        return False, "Место проведения не заполнено"

    if len(str(place).strip()) > 256:
        return False, "Место проведения слишком длинное"

    is_valid, message = validate_id(level)
    if not is_valid:
        return False, f"Некорректный уровень: {message}"

    is_valid, message = validate_date(event_date)
    if not is_valid:
        return False, message

    is_valid, message = validate_id(event_type)
    if not is_valid:
        return False, f"Некорректный тип мероприятия: {message}"

    is_valid, message = validate_id(control)
    if not is_valid:
        return False, f"Некорректный контроль: {message}"

    if description is not None and len(str(description)) > 1000:
        return False, "Описание слишком длинное"

    return True, ""
