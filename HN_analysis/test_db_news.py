import pytest
import os
import db_store as dbs
import db_news as dbn
import os.path as op

#checking if the file exsits in the filesystem
def check_if_file_exists(fname):
    return op.exists(fname)

def execute_short_db(fname, query):
    ret = None
    with dbs.SQLCursor(fname) as cur:
        ex = cur.execute(query)
        ret = ex.fetchall()

    return ret

#checking if the table exists in the DB
def check_if_table_exsits(fname, table):
    ret = 0

    ex = execute_short_db(fname,
            "SELECT name FROM sqlite_master WHERE type='table' AND name = '" + table + "'")
    if ex is not None:
        ret = len(ex)

    return ret

#template for 2 tests checking the init_db parameters
def template_test_init_db(fname="news.db", tabname="News"):
    fname_tmp = fname+".orig"

    #setup test
    if check_if_file_exists(fname):
        os.rename(fname, fname_tmp)

    #test default 
    if fname == "news.db":
        dbn.init_news_database()
    else: 
        dbn.init_news_database(fname)
    assert(True == check_if_file_exists(fname))
    assert(1 == check_if_table_exsits(fname, tabname))

    #cleanup test
    os.remove(fname)
    if check_if_file_exists(fname_tmp):
        os.rename(fname_tmp, fname)

#/////////////////// Tests /////////////////////
def test_init_db():
    template_test_init_db()
    template_test_init_db(fname="random.db")

def test_store():
    fname = "random.db"
    sq = dbn.init_news_database(fname)

    news = [
            (1, "Test1", "10-01-1990"),
            (2, "Test2", "10-02-1990"),
            (3, "Test3", "10-03-1990"),
            (4, "Test4", "10-04-1990"),
            (5, "Test5", "10-05-1990"),
            ]
    dbn.store_news_batch(sq, news)

    ex = execute_short_db(fname,
            "SELECT id FROM News WHERE id < 5")
    assert(ex is not None)
    assert(4 == len(ex))

    ex = execute_short_db(fname,
            "SELECT id FROM News")
    assert(ex is not None)
    assert(5 == len(ex))

    sq.getconnection().close()
    os.remove(fname)

def test_max_id():
    fname = "random.db"
    sq = dbn.init_news_database(fname)

    news = [
            (1123, "Test1", "10-01-1990"),
            (2, "Test2", "10-02-1990"),
            (3, "Test3", "10-03-1990"),
            (334, "Test4", "10-04-1990"),
            (1328975, "Test5", "10-05-1990"),
            ]
    dbn.store_news_batch(sq, news)
    
    mid = dbn.get_max_id(sq)
    assert(1328975 == mid[0])

    sq.getconnection().close()
    os.remove(fname)



