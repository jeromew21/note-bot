import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet 

STOPWORDS = set(stopwords.words("english"))

def synsets(word):
    for syn in wordnet.synsets(word): 
        yield syn

keywords = [
    wordnet.synset("take.v.01"),
    wordnet.synset("retrieve.v.02"),
    wordnet.synset("delete.v.01"),
    wordnet.synset('total.v.01'),
]

#for vec in keyword_vectors:
 #   for i in range(len(vec)):
  #      for syn in synonyms(vec[i]):
   #         vec.append(syn)

def tokenize(sentence):
    sentence = "".join([i for i in sentence.lower() if i in "qwertyuiopasdfghjklzxcvbnm "])
    tokens = nltk.word_tokenize(sentence)
    return [t for t in tokens if t not in STOPWORDS]

def classify(tokens):
    max_max_word_similarity = -1000
    max_keyword_index = 0
    for i, synset in enumerate(keywords):
        max_word_similarity = -10000
        for word in tokens:
            similarity = sum([synset.path_similarity(ss) for ss in synsets(word)])
            if similarity > max_word_similarity:
                max_word_similarity = similarity
        if max_word_similarity > max_max_word_similarity:
            max_max_word_similarity = max_word_similarity
            max_keyword_index = i
    return max_keyword_index
