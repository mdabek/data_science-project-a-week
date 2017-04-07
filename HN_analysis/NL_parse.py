import nltk
import re
from nltk.corpus import stopwords
from nltk import FreqDist

def clean_and_tag_word_token(text):
	raw_tokenized_text = nltk.word_tokenize(text)
	#Filter out stopwords
	tokenized_text = [token for token in raw_tokenized_text if token not in stopwords.words('english')]
	cleaned_tagged_text = [word for word in nltk.pos_tag(tokenized_text) if re.match('\w', word[0])]

	return cleaned_tagged_text

def clean_and_chunk(text):
	#raw_tokenized_text = nltk.word_tokenize(text)
	#Filter out stopwords
	#tokenized_text = [token for token in raw_tokenized_text if token not in stopwords.words('english')]
	#cleaned_tagged_text = [word for word in nltk.pos_tag(tokenized_text) if re.match('\w', word[0])]

	return 0#cleaned_tagged_text
	
	
def most_common_words(text, count):
	fdist = FreqDist(text)
	return fdist.most_common(count)