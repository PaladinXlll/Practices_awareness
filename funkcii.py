from database import get_connection #сдесь ссылка на бд

def add_data(table, values):
    conn = get_connection()
    cursor = conn.cursor()

    placeholders = ", ".join(["?"] * len(values))
    query = f"INSERT INTO {table} VALUES (NULL, {placeholders})"

    cursor.execute(query, values)

    conn.commit()
    conn.close()


def delete_data(table, record_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = f"DELETE FROM {table} WHERE id = ?"
    cursor.execute(query, (record_id,))

    conn.commit()
    conn.close()


def update_data(table, record_id, column, new_value):
    conn = get_connection()
    cursor = conn.cursor()

    query = f"UPDATE {table} SET {column} = ? WHERE id = ?"
    cursor.execute(query, (new_value, record_id))

    conn.commit()
    conn.close()
    