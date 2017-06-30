import requests
import json
import NL_parse as nlp
import matplotlib.pyplot as plt
import pandas as pd
import db_store as dbs


def store_news(id, date, title):
    try:
        dbs.store_news(id, date, title)
    except:
        pass

def retrieve_news(id):
    try:
        dbs.retrieve_news()
    except:
        raise

def run_per_token_analysis(tokens):

    top_count = 10
    #list of nouns
    nouns_tagged = [token for token in tokens if token[1].startswith('NN')]
    nouns_top10 = [(top10[0][0], top10[1]) for top10 in nlp.most_common_words(nouns_tagged, top_count)]

    #list of verbs
    verbs_tagged = [token for token in tokens if token[1].startswith('VB')]
    verbs_top10 = [(top10[0][0], top10[1]) for top10 in nlp.most_common_words(verbs_tagged, top_count)]

    #list of adjectives
    adjectives_tagged = [token for token in tokens if token[1].startswith('J')]
    adjectives_top10 = [(top10[0][0], top10[1]) for top10 in nlp.most_common_words(adjectives_tagged, top_count)]

    ## Plot the results
    ## Consider makint it a separtate function
    label_count = 'count'
    label_word = 'word'

    nouns_top10_df = pd.DataFrame(nouns_top10, columns=[label_word, label_count])
    verbs_top10_df = pd.DataFrame(verbs_top10, columns=[label_word, label_count])
    adjectives_top10_df = pd.DataFrame(adjectives_top10, columns=[label_word, label_count])

    plt.figure(1)
    plt.subplot(311)
    plt.bar(left=range(10), height=nouns_top10_df[label_count], color='#fca3fc', alpha=0.8, tick_label=nouns_top10_df[label_word])
    plt.subplot(312)
    plt.bar(left=range(10), height=verbs_top10_df[label_count], color='#ffaec9', alpha=0.8, tick_label=verbs_top10_df[label_word])
    plt.subplot(313)
    plt.bar(left=range(10), height=adjectives_top10_df[label_count], color='#f246c8', alpha=0.8, tick_label=adjectives_top10_df[label_word])
    plt.show()

def update_news_db():
    url = "https://hacker-news.firebaseio.com/v0/newstories.json?print=pretty"
    news = []
    cursor = None

    response=requests.get(url)

    try :
        cursor = dbs.init_database()
        max_id = dbs.get_max_id(cursor)

        ## Check GET response and if OK, read single news item
        if response.ok:
            jdata = response.json()

            gen = [key for key in jdata if max_id[0] is None or max_id[0] < int(str(key))]

            for key in gen :
                item_url = "https://hacker-news.firebaseio.com/v0/item/" + str(key) + ".json?print=pretty"
                item_response = requests.get(item_url)

                ## Add text to a single title - corpora
                if item_response.ok:
                    news.append((item_response.json()['id'], item_response.json()['title'], item_response.json()['time']))

        if len(news) > 0:
            dbs.store_news_batch(cursor, news)

    finally:
        if cursor is not None:
            cursor.connection.close()

def get_database_data(sql_filter = ""):

    titles = ' '
    cursor = None

    try :
        cursor = dbs.get_cursor()

        raw_db_data = dbs.retrieve_news_titles(cursor, sql_filter)

        for title in raw_db_data:
            titles += title[0] + " "
    finally:
        if cursor is not None:
            cursor.connection.close()

    return titles


## On start: update database with latest news
update_news_db()
## Create a single text corpora from headers

texts = get_database_data()

## 2. Tokenize texts to words and tag words. Next, run analysis showing 10 most popular words for
##	  nouns, verbs, adjectives. Also, draw plots, since plots are crucial! 
tagged_word_tokens = nlp.clean_and_tag_word_token(texts)
run_per_token_analysis(tagged_word_tokens)

## 3. Tokenize texts to words and tag words. Next, run analysis showing 10 most popular words for nouns, verbs, adjectives
## chunk_text = nlp.clean_and_chunk(texts)
#run_per_chunk_analysis(tokens)