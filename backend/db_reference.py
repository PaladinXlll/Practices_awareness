from db_functions import get_data
from validators import validate_id


def get_levels():
    return get_data(
        table="level",
        columns=["level_id", "name"]
    )


def get_level_by_id(level_id):
    is_valid, message = validate_id(level_id)

    if not is_valid:
        print(message)
        return None

    return get_data(
        table="level",
        record_id=level_id,
        columns=["level_id", "name"]
    )


def get_types():
    return get_data(
        table="type",
        columns=["type_id", "name"]
    )


def get_type_by_id(type_id):
    is_valid, message = validate_id(type_id)

    if not is_valid:
        print(message)
        return None

    return get_data(
        table="type",
        record_id=type_id,
        columns=["type_id", "name"]
    )


def get_controls():
    return get_data(
        table="control",
        columns=["control_id", "name"]
    )


def get_control_by_id(control_id):
    is_valid, message = validate_id(control_id)

    if not is_valid:
        print(message)
        return None

    return get_data(
        table="control",
        record_id=control_id,
        columns=["control_id", "name"]
    )

if __name__ == "__main__":
    print("LEVELS:")
    print(get_levels())

    print("LEVEL BY ID:")
    print(get_level_by_id(1))

    print("TYPES:")
    print(get_types())

    print("TYPE BY ID:")
    print(get_type_by_id(1))

    print("CONTROLS:")
    print(get_controls())

    print("CONTROL BY ID:")
    print(get_control_by_id(1))


