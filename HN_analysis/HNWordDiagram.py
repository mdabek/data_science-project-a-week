import requests
import json
import NL_parse as nlp
import matplotlib.pyplot as plt
import pandas as pd

def read_news_from_file():
	try:
		f = open('news_textfile.txt', 'r')
		texts = f.read()
		f.close()
	except FileNotFoundError:
		return ""
	return texts

def write_news_to_text(texts):
	try:
		f = open('news_textfile.txt', 'w')
		f.write(texts)
		f.close()
	except:
		pass

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
	
def read_news():
	url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
	texts = ""
	response=requests.get(url)
	
	## Check GET response and if OK, read single news item
	if response.ok:
		jdata = response.json()
	
		for key in jdata:
			print('.')
			item_url = "https://hacker-news.firebaseio.com/v0/item/" + str(key) + ".json?print=pretty"
			item_response = requests.get(item_url)
			
			## Add text to a single title - corpora
			if item_response.ok:
				texts += " " + ascii(item_response.json()['title'])
	
	return texts
	

## 1. Read news from file and if there are none, read news using ycombinator news REST API.
##    Itsy-bitsy optimization - save the news to a file!
texts = read_news_from_file()
if texts == "":
	texts = read_news()
	if texts != "":
		write_news_to_text(texts)

## 2. Tokenize texts to words and tag words. Next, run analysis showing 10 most popular words for 
##	  nouns, verbs, adjectives. Also, draw plots, since plots are crucial! 
tagged_word_tokens = nlp.clean_and_tag_word_token(texts)
run_per_token_analysis(tagged_word_tokens)

## 3. Tokenize texts to words and tag words. Next, run analysis showing 10 most popular words for nouns, verbs, adjectives
#chunk_text = nlp.clean_and_chunk(texts)
#run_per_chunk_analysis(tokens)