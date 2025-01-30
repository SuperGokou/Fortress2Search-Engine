import time
import Database
import re
import string


def querySearch(query):
    s = time.time()

    # query filter
    Database.dataBaseSetUp()
    p = re.compile("[" + re.escape(string.punctuation) + "]")
    query = p.sub(" ", query)
    # query filter if conatains '%$&\/'

    command_select_table = ('''SELECT   highlight(items,1, '<b>', '</b>')Name, 
                                        highlight(items,2, '<b>', '</b>')CustomName,
                                        highlight(items,3, '<b>', '</b>')Quality,
                                        highlight(items,4, '<b>', '</b>')Description, 
                                        highlight(items,5, '<b>', '</b>')ItemHeader, 
                                        highlight(items,6, '<b>', '</b><br>')Class,
                                        WikiId, OwnerUrl, OwnerSteamId, IconId 
                                FROM items
                                WHERE items MATCH " %s " 
                                ''' % query)
    Database.cursor.execute(command_select_table)
    result = Database.cursor.fetchall()

    e = time.time()
    costtime = e - s

    return result, costtime


def queryBM25Search(query):
    s = time.time()

    # query filter
    Database.dataBaseSetUp()
    p = re.compile("[" + re.escape(string.punctuation) + "]")
    query = p.sub(" ", query)
    # query filter if conatains '%$&\/'

    command_select_table = ('''SELECT   highlight(items,1, '<b>', '</b>')Name, 
                                        highlight(items,2, '<b>', '</b>')CustomName,
                                        highlight(items,3, '<b>', '</b>')Quality,
                                        highlight(items,4, '<b>', '</b>')Description, 
                                        highlight(items,5, '<b>', '</b>')ItemHeader, 
                                        highlight(items,6, '<b>', '</b><br>')Class,
                                        WikiId, OwnerUrl, OwnerSteamId, IconId 
                                FROM items
                                WHERE items MATCH " %s " 
                                ORDER BY bm25(items)
                                ''' % query)
    Database.cursor.execute(command_select_table)
    result = Database.cursor.fetchall()

    e = time.time()
    costtime = e - s

    return result, costtime


def queryWikiIdSearch(query):
    s = time.time()

    # query filter
    Database.dataBaseSetUp()
    p = re.compile("[" + re.escape(string.punctuation) + "]")
    query = p.sub(" ", query)
    # query filter if conatains '%$&\/'

    command_select_table = ('''SELECT   highlight(items,1, '<b>', '</b>')Name, 
                                        highlight(items,2, '<b>', '</b>')CustomName,
                                        highlight(items,3, '<b>', '</b>')Quality,
                                        highlight(items,4, '<b>', '</b>')Description, 
                                        highlight(items,5, '<b>', '</b>')ItemHeader, 
                                        highlight(items,6, '<b>', '</b><br>')Class,
                                        WikiId, OwnerUrl, OwnerSteamId, IconId 
                                FROM items
                                WHERE items MATCH " %s " 
                                ORDER BY (WikiId)
                                ''' % query)
    Database.cursor.execute(command_select_table)
    result = Database.cursor.fetchall()

    e = time.time()
    costtime = e - s

    return result, costtime


def queryFrqsearch(query):
    s = time.time()
    # query filter
    Database.dataBaseSetUp()
    p = re.compile("[" + re.escape(string.punctuation) + "]")
    query = p.sub(" ", query)
    # query filter if conatains '%$&\/'

    command_select_table = ('''SELECT   highlight(items,1, '<b>', '</b>')Name,
                                        highlight(items,2, '<b>', '</b>')CustomName,
                                        highlight(items,3, '<b>', '</b>')Quality,
                                        highlight(items,4, '<b>', '</b>')Description,
                                        highlight(items,5, '<b>', '</b>')ItemHeader,
                                        highlight(items,6, '<b>', '</b><br>')Class,
                                        WikiId, OwnerUrl, OwnerSteamId, IconId
                                FROM items
                                WHERE items MATCH " %s "
                                ORDER BY RANK
                                ''' % query)
    Database.cursor.execute(command_select_table)
    result = Database.cursor.fetchall()

    e = time.time()
    costtime = e - s

    return result, costtime