import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet 

STOPWORDS = set(stopwords.words("english"))

def synsets(word):
    for syn in wordnet.synsets(word): 
        yield syn

keywords = [
    [wordnet.synset("take.v.01")],
    [wordnet.synset("retrieve.v.02"), wordnet.synset("get.v.01")],
    [wordnet.synset("delete.v.01"), wordnet.synset("remove.v.01")],
    [wordnet.synset('total.v.01'), wordnet.synset("many.a.01")],
]

#for vec in keyword_vectors:
 #   for i in range(len(vec)):
  #      for syn in synonyms(vec[i]):
   #         vec.append(syn)

def tokenize_bigrams(sentence):
    sentence = "".join([i for i in sentence.lower() if i in "qwertyuiopasdfghjklzxcvbnm "])
    tokens = nltk.word_tokenize(sentence)
    return tokens

def tokenize(sentence):
    sentence = "".join([i for i in sentence.lower() if i in "qwertyuiopasdfghjklzxcvbnm "])
    tokens = nltk.word_tokenize(sentence)
    return [t for t in tokens if t not in STOPWORDS]

def classify(tokens):
    max_max_word_similarity = -1000
    max_keyword_index = 0
    for i, synset_list in enumerate(keywords):
        max_word_similarity = -10000
        max_word = None
        for synset in synset_list:
            for word in tokens:
                to_sum = [synset.wup_similarity(ss) for ss in synsets(word)]
                to_sum = [0 if k is None else k for k in to_sum]
                similarity = sum(to_sum)/len(to_sum) #Mean
                if similarity > max_word_similarity:
                    max_word_similarity = similarity
                    max_word = word
        if max_word_similarity > max_max_word_similarity:
            max_max_word_similarity = max_word_similarity
            max_keyword_index = i
    return max_keyword_index