import Database


def autoComplete():
    Database.dataBaseSetUp()

    command_select_table = ('''SELECT   Name, 
                                        CustomName
                                FROM items''')

    Database.cursor.execute(command_select_table)
    automata_data = Database.cursor.fetchall()

    return automata_data
