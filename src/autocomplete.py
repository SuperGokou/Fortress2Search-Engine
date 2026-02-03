"""Autocomplete module for Team Fortress 2 Search Engine."""

from . import database


def get_suggestions():
    """Fetch item names for autocomplete suggestions."""
    conn, cursor = database.get_connection()

    sql = '''SELECT Name, CustomName FROM items'''

    try:
        cursor.execute(sql)
        data = cursor.fetchall()
    except Exception:
        data = []
    finally:
        conn.close()

    return data
