"""Database module for Team Fortress 2 Search Engine."""

import sqlite3
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'mainitem.db')
CSV_PATH = os.path.join(BASE_DIR, 'data', 'formattedDataset.csv')

_initialized = False


def get_connection():
    """Get a database connection and cursor. Caller is responsible for closing."""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    ensure_database_setup(connection, cursor)
    return connection, cursor


def ensure_database_setup(connection, cursor):
    """Ensure the database table exists, create if needed."""
    global _initialized

    if _initialized:
        return

    cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='items' ''')

    if cursor.fetchone()[0] == 1:
        _initialized = True
        return

    cursor.execute('''DROP TABLE IF EXISTS items''')
    command_create_table = '''CREATE VIRTUAL TABLE items USING fts5(
        Id, Name, CustomName, Quality, Description,
        ItemHeader, Class, WikiId, OwnerUrl, OwnerSteamId, IconId,
        tokenize = 'porter ascii'
    )'''

    cursor.execute(command_create_table)

    if not os.path.exists(CSV_PATH):
        connection.commit()
        _initialized = True
        return

    df = pd.read_csv(CSV_PATH)

    columns = ['Id', 'Name', 'CustomName', 'Quality', 'Description', 'ItemHeader',
               'Class', 'WikiId', 'OwnerUrl', 'OwnerSteamId', 'IconId']

    df.drop(df.query(
        'Id.isnull() | CustomName.isnull() | Quality.isnull() | '
        'Class.isnull() | WikiId.isnull() | OwnerUrl.isnull() | '
        'OwnerSteamId.isnull() | IconId.isnull() | Name.isnull()'
    ).index, inplace=True)

    df_row_data = df[columns]
    rows_data = df_row_data.values.tolist()

    command_insert_data = '''INSERT INTO items (
        Id, Name, CustomName, Quality, Description, ItemHeader,
        Class, WikiId, OwnerUrl, OwnerSteamId, IconId
    ) VALUES (?,?,?,?,?,?,?,?,?,?,?)'''

    for row_data in rows_data:
        try:
            cursor.execute(command_insert_data, row_data)
        except Exception as e:
            print('Insert error: %s (in %s)' % (e, row_data))
            continue

    connection.commit()
    _initialized = True
