from db_functions import execute_select

TABLE_EVENTS = "event"
TABLE_LINK = "teachers_events"


def filter_events_by_teacher(teacher_id):
    query = f"""
        SELECT e.*
        FROM {TABLE_EVENTS} e
        JOIN {TABLE_LINK} te ON e.event_id = te.event
        WHERE te.teacher = %s
    """

    return execute_select(query, (teacher_id,))


def filter_events_by_year(year):
    query = f"""
        SELECT *
        FROM {TABLE_EVENTS}
        WHERE YEAR(event_date) = %s
    """

    return execute_select(query, (year,))


def filter_events_by_semester(semester):
    if semester == 1:
        query = f"""
            SELECT *
            FROM {TABLE_EVENTS}
            WHERE MONTH(event_date) BETWEEN 1 AND 6
        """
    else:
        query = f"""
            SELECT *
            FROM {TABLE_EVENTS}
            WHERE MONTH(event_date) BETWEEN 9 AND 12
        """

    return execute_select(query)


def filter_events_by_level(level_id):
    query = f"""
        SELECT *
        FROM {TABLE_EVENTS}
        WHERE level = %s
    """

    return execute_select(query, (level_id,))


def filter_events_by_type(type_id):
    query = f"""
        SELECT *
        FROM {TABLE_EVENTS}
        WHERE type = %s
    """

    return execute_select(query, (type_id,))


def filter_events_by_control(control_id):
    query = f"""
        SELECT *
        FROM {TABLE_EVENTS}
        WHERE control = %s
    """

    return execute_select(query, (control_id,))


def search_events_by_name(name):
    query = f"""
        SELECT *
        FROM {TABLE_EVENTS}
        WHERE name LIKE %s
    """

    search_pattern = f"%{name}%"

    return execute_select(query, (search_pattern,))


def get_filtered_events(filters: dict):
    column_mapping = {
        "level_id": "level",
        "type_id": "type",
        "control_id": "control"
    }

    conditions = []
    values = []

    if filters.get("teacher_id"):
        query = f"""
            SELECT e.*
            FROM {TABLE_EVENTS} e
            JOIN {TABLE_LINK} te ON e.event_id = te.event
            WHERE 1=1
        """

        conditions.append("te.teacher = %s")
        values.append(filters["teacher_id"])

    else:
        query = f"""
            SELECT e.*
            FROM {TABLE_EVENTS} e
            WHERE 1=1
        """

    for filter_key, db_column in column_mapping.items():
        if filter_key in filters and filters[filter_key] is not None:
            conditions.append(f"e.{db_column} = %s")
            values.append(filters[filter_key])

    if filters.get("year"):
        conditions.append("YEAR(e.event_date) = %s")
        values.append(filters["year"])

    if filters.get("semester"):
        if filters["semester"] == 1:
            conditions.append("MONTH(e.event_date) BETWEEN 1 AND 6")
        else:
            conditions.append("MONTH(e.event_date) BETWEEN 9 AND 12")

    if filters.get("name"):
        conditions.append("e.name LIKE %s")
        values.append(f"%{filters['name']}%")

    if conditions:
        query += " AND " + " AND ".join(conditions)

    return execute_select(query, tuple(values))


