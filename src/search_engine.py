"""Search engine module for Team Fortress 2 items."""

import time
import re
import string
from . import database


def sanitize_query(query):
    """Sanitize query for FTS5 MATCH - remove special characters that could cause issues."""
    p = re.compile("[" + re.escape(string.punctuation) + "]")
    query = p.sub(" ", query)
    query = " ".join(query.split())
    return query


def query_search(query):
    """Execute a basic search query."""
    start = time.time()

    conn, cursor = database.get_connection()
    query = sanitize_query(query)

    if not query.strip():
        return [], 0

    sql = '''SELECT highlight(items,1, '<b>', '</b>') AS Name,
                    highlight(items,2, '<b>', '</b>') AS CustomName,
                    highlight(items,3, '<b>', '</b>') AS Quality,
                    highlight(items,4, '<b>', '</b>') AS Description,
                    highlight(items,5, '<b>', '</b>') AS ItemHeader,
                    highlight(items,6, '<b>', '</b><br>') AS Class,
                    WikiId, OwnerUrl, OwnerSteamId, IconId
             FROM items
             WHERE items MATCH ?'''

    try:
        cursor.execute(sql, (query,))
        result = cursor.fetchall()
    except Exception:
        result = []
    finally:
        conn.close()

    elapsed = time.time() - start
    return result, elapsed


def query_bm25_search(query):
    """Execute a search query with BM25 ranking."""
    start = time.time()

    conn, cursor = database.get_connection()
    query = sanitize_query(query)

    if not query.strip():
        return [], 0

    sql = '''SELECT highlight(items,1, '<b>', '</b>') AS Name,
                    highlight(items,2, '<b>', '</b>') AS CustomName,
                    highlight(items,3, '<b>', '</b>') AS Quality,
                    highlight(items,4, '<b>', '</b>') AS Description,
                    highlight(items,5, '<b>', '</b>') AS ItemHeader,
                    highlight(items,6, '<b>', '</b><br>') AS Class,
                    WikiId, OwnerUrl, OwnerSteamId, IconId
             FROM items
             WHERE items MATCH ?
             ORDER BY bm25(items)'''

    try:
        cursor.execute(sql, (query,))
        result = cursor.fetchall()
    except Exception:
        result = []
    finally:
        conn.close()

    elapsed = time.time() - start
    return result, elapsed


def query_wiki_id_search(query):
    """Execute a search query ordered by WikiId."""
    start = time.time()

    conn, cursor = database.get_connection()
    query = sanitize_query(query)

    if not query.strip():
        return [], 0

    sql = '''SELECT highlight(items,1, '<b>', '</b>') AS Name,
                    highlight(items,2, '<b>', '</b>') AS CustomName,
                    highlight(items,3, '<b>', '</b>') AS Quality,
                    highlight(items,4, '<b>', '</b>') AS Description,
                    highlight(items,5, '<b>', '</b>') AS ItemHeader,
                    highlight(items,6, '<b>', '</b><br>') AS Class,
                    WikiId, OwnerUrl, OwnerSteamId, IconId
             FROM items
             WHERE items MATCH ?
             ORDER BY WikiId'''

    try:
        cursor.execute(sql, (query,))
        result = cursor.fetchall()
    except Exception:
        result = []
    finally:
        conn.close()

    elapsed = time.time() - start
    return result, elapsed


def query_frequency_search(query):
    """Execute a search query ordered by frequency rank."""
    start = time.time()

    conn, cursor = database.get_connection()
    query = sanitize_query(query)

    if not query.strip():
        return [], 0

    sql = '''SELECT highlight(items,1, '<b>', '</b>') AS Name,
                    highlight(items,2, '<b>', '</b>') AS CustomName,
                    highlight(items,3, '<b>', '</b>') AS Quality,
                    highlight(items,4, '<b>', '</b>') AS Description,
                    highlight(items,5, '<b>', '</b>') AS ItemHeader,
                    highlight(items,6, '<b>', '</b><br>') AS Class,
                    WikiId, OwnerUrl, OwnerSteamId, IconId
             FROM items
             WHERE items MATCH ?
             ORDER BY RANK'''

    try:
        cursor.execute(sql, (query,))
        result = cursor.fetchall()
    except Exception:
        result = []
    finally:
        conn.close()

    elapsed = time.time() - start
    return result, elapsed
