from db_functions import get_data, add_data, update_data, delete_data


TABLE_NAME = "event"

COLUMNS = [
    "event_id",
    "name",
    "place",
    "level",
    "event_date",
    "document",
    "type",
    "control",
    "description"
]


def get_events():
    """
    Получить все мероприятия.
    """
    return get_data(
        table=TABLE_NAME,
        columns=COLUMNS
    )


def get_event_by_id(event_id):
    """
    Получить мероприятие по ID.
    """
    return get_data(
        table=TABLE_NAME,
        record_id=event_id,
        columns=COLUMNS
    )


def add_event(
    name,
    place,
    level,
    event_date,
    document,
    type,
    control,
    description
):
    """
    Добавить мероприятие.
    """
    return add_data(
        table=TABLE_NAME,
        columns=[
            "name",
            "place",
            "level",
            "event_date",
            "document",
            "type",
            "control",
            "description"
        ],
        values=[
            name,
            place,
            level,
            event_date,
            document,
            type,
            control,
            description
        ]
    )


def update_event(
    event_id,
    name,
    place,
    level,
    event_date,
    document,
    type,
    control,
    description
):
    """
    Обновить мероприятие.
    """
    return update_data(
        table=TABLE_NAME,
        record_id=event_id,
        update_values={
            "name": name,
            "place": place,
            "level": level,
            "event_date": event_date,
            "document": document,
            "type": type,
            "control": control,
            "description": description
        }
    )


def delete_event(event_id):
    """
    Удалить мероприятие.
    """
    return delete_data(
        table=TABLE_NAME,
        record_id=event_id
    )

