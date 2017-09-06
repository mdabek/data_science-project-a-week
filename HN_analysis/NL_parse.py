import nltk
import re
from nltk.corpus import stopwords
from nltk import FreqDist
from nltk.tokenize import sent_tokenize

def clean_and_tag_word_token(text):
    raw_tokenized_text = nltk.word_tokenize(text)
    #Filter out stopwords
    updated_stopwords = stopwords.words('english')
    #Typical HN titles are Ask HN and Show HN these skew results - we need to drop them
    updated_stopwords.extend(['HN','Ask', 'Show'])

        
    tokenized_text = [token for token in raw_tokenized_text if token not in updated_stopwords]
    cleaned_tagged_text = [word for word in nltk.pos_tag(tokenized_text) if re.match('\w', word[0])]

    return cleaned_tagged_text

def clean_and_chunk(text, grammar = "NP:{<NN.*><NN.*>}"):
    chunks = []
    
    chunk_parser = nltk.RegexpParser(grammar)

    sentences = sent_tokenize(text)
    
    for sentence in sentences :
        tagged_sentence = clean_and_tag_word_token(sentence)
        chunks.append(chunk_parser.parse(tagged_sentence))
    
    return chunks

    
def most_common_words(text, count):
    fdist = FreqDist(text)
    return fdist.most_common(count)
