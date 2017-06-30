import sqlite3 as sq3

def get_max_id(cursor) :
    ex = cursor.execute("SELECT MAX(id) FROM News")
    return ex.fetchone()

def store_news_batch(cursor, news):
    cursor.executemany("INSERT INTO News VALUES(?,?, datetime(?, 'unixepoch'))", news)
    cursor.connection.commit()

def retrieve_news_titles(cursor, sql_filter):

    where_statement = ""

    if sql_filter is not "":
        where_statement = " WHERE " + sql_filter

    sql_query = "SELECT Title FROM News" + where_statement

    ex = cursor.execute(sql_query)

    return ex.fetchall()

def get_cursor():
    conn = None
    cur = None
    try:
        conn = sq3.connect("news.db")
        cur = conn.cursor()
    except:
        if conn is not None:
            conn.close()

    return cur

def init_database():
    cur = None

    try:
        cur = get_cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS News(Id INTEGER PRIMARY KEY, Title TEXT, PostTime DATETIME)")

    except:
        if cur is not None:
            cur.connection.close()
        raise

    return cur