import sqlite3
import sys
import pandas as pd


# Id,Name,CustomName,Quality,Description,ItemHeader,Class,WikiId,OwnerUrl,OwnerSteamId,IconId


def dataBaseSetUp():
    connection = sqlite3.connect('mainitem.db')
    global cursor
    cursor = connection.cursor()
    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='items' ''')

    if cursor.fetchone()[0] == 1:
        print('Database connected')

    else:
        cursor.execute('''DROP TABLE IF EXISTS items ''')
        command_create_table = '''CREATE VIRTUAL TABLE items USING fts5(Id, Name, CustomName, Quality, Description, 
                                    ItemHeader, Class, WikiId, OwnerUrl, OwnerSteamId, IconId, 
                                    tokenize = 'porter ascii')'''

        cursor.execute(command_create_table)

        df = pd.read_csv('formattedDataset.csv')

        column = ['Id', 'Name', 'CustomName', 'Quality', 'Description', 'ItemHeader',
                  'Class', 'WikiId', 'OwnerUrl', 'OwnerSteamId', 'IconId']

        # clean the data each column filter null and place it
        df.drop(df.query('Id.isnull() | CustomName.isnull() | Quality.isnull()'
                         '|Class.isnull() | WikiId.isnull() | OwnerUrl.isnull() | OwnerSteamId.isnull()'
                         '|IconId.isnull() | Name.isnull()').index, inplace=True)

        df_row_data = df[column]
        rows_data = df_row_data.values.tolist()

        command_insert_data = ''' INSERT INTO items ('Id', 'Name', 'CustomName', 'Quality', 'Description', 'ItemHeader',
                      'Class', 'WikiId', 'OwnerUrl', 'OwnerSteamId', 'IconId') VALUES (?,?,?,?,?,?,?,?,?,?,?)'''

        for row_data in rows_data:
            try:
                cursor.execute(command_insert_data, row_data)
            except:
                e = sys.exc_info()[0]
                print('Insert error %s (in %s)' % (e, row_data))
                continue

        connection.commit()
