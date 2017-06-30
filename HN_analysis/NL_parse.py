import nltk
import re
from nltk.corpus import stopwords
from nltk import FreqDist
from nltk.tokenize import moses

def clean_and_tag_word_token(text):
	raw_tokenized_text = nltk.word_tokenize(text)
	#Filter out stopwords
	tokenized_text = [token for token in raw_tokenized_text if token not in stopwords.words('english')]
	cleaned_tagged_text = [word for word in nltk.pos_tag(tokenized_text) if re.match('\w', word[0])]

	return cleaned_tagged_text

def clean_and_chunk(text, grammar = "NP:{<DT|PP\$>?<JJ>*<NN.*><NN.*>?}"):
	tokenizer = moses.MosesTokenizer()
	chunks = []
	
	chunk_parser = nltk.RegexpParser(grammar)
	
	for sentence in text :
		tagged_sentence = clean_and_tag_word_token(sentence)
		chunks.append(chunk_parser.parse(tagged_sentence))
	
	return chunks

	
def most_common_words(text, count):
	fdist = FreqDist(text)
	return fdist.most_common(count)