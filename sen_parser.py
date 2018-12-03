import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet 

STOPWORDS = set(stopwords.words("english"))
STOPWORDS.add("please")

def synsets(word):
    for syn in wordnet.synsets(word): 
        yield syn

# Maps POS tags to wordnet equivalent tag
POS_MAPPING = {
    'NN': 'n',
    'NNS': 'n',
    'NNP': 'n',
    'NNPS': 'n',
    'VB': 'v',
    'VBD': 'v',
    'VBG': 'v',
    'VBN': 'v',
    'VBP': 'v',
    'VBZ': 'v',
    'JJ': 'a',
    'JJR': 'a',
    'JJS': 'a'
}

keywords = [
    [wordnet.synset("take.v.01")],
    [wordnet.synset("retrieve.v.02"), wordnet.synset("last.n.02")],
    [wordnet.synset("delete.v.01"), wordnet.synset("remove.v.01")],
    [wordnet.synset("total.v.01"), wordnet.synset("many.a.01")],
]

def pos_tag_to_wordnet_tag(tag):
    """ Takes POS tag from NLTK and returns equivalent wordnet tag and None if not verb, noun, or adj """

    return POS_MAPPING.get(tag, None)

def tokenize_bigrams(sentence):
    """ Tokenizes sentence into bigrams. """
    sentence = "".join([i for i in sentence.lower() if i in "qwertyuiopasdfghjklzxcvbnm "])
    tokens = nltk.word_tokenize(sentence)
    return tokens

def tokenize(sentence):
    """ Tokenizes sentence. """
    sentence = "".join([i for i in sentence.lower() if i in "qwertyuiopasdfghjklzxcvbnm "])
    tokens = nltk.word_tokenize(sentence)
    return [t for t in tokens if t not in STOPWORDS]

def classify(tokens):
    """ Classifies sentence by it's tokens. Returns a value desired command. """
    threshold = 0.20
    max_max_word_similarity = -1000
    max_keyword_index = 0
    max_max_word = None
    for i, synset_list in enumerate(keywords):
        max_word_similarity = -10000
        max_word = None
        for word in tokens:
            for synset in synset_list:
                #FILTER BY PART OF SPEECH
                to_sum = [synset.wup_similarity(ss) for ss in synsets(word)][:8] #Cutoff
                to_sum = [0 if k is None else k for k in to_sum]
                decay = 1
                for j, _ in enumerate(to_sum): #Decay similarity
                    to_sum[j] *= decay
                    decay *= 0.9 #Decay amount
                if len(to_sum) > 0:
                    similarity = sum(to_sum)/len(to_sum) #Mean
                    if similarity > max_word_similarity:
                        max_word_similarity = similarity
                        max_word = word
        if max_word_similarity > max_max_word_similarity:
            max_max_word_similarity = max_word_similarity
            max_keyword_index = i
            max_max_word = max_word
            #print(max_max_word, max_word_similarity, max_keyword_index)
    if max_max_word_similarity < threshold:
        return -1
    return max_keyword_index


def text2int(textnum, numwords={}):
    """ Converts a cardinal or ordinal number to it's numerical counterpart. """
    if not numwords:
        units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
        ]

        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

        scales = ["hundred", "thousand", "million", "billion", "trillion"]

        numwords["and"] = (1, 0)
        for idx, word in enumerate(units):  numwords[word] = (1, idx)
        for idx, word in enumerate(tens):       numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales): numwords[word] = (10 ** (idx * 3 or 2), 0)

    ordinal_words = {'first':1, 'second':2, 'third':3, 'fifth':5, 'eighth':8, 'ninth':9, 'twelfth':12}
    ordinal_endings = [('ieth', 'y'), ('th', '')]

    textnum = textnum.replace('-', ' ')

    current = result = 0
    for word in textnum.split():
        if word in ordinal_words:
            scale, increment = (1, ordinal_words[word])
        else:
            for ending, replacement in ordinal_endings:
                if word.endswith(ending):
                    word = "%s%s" % (word[:-len(ending)], replacement)

            if word not in numwords:
                raise Exception("Illegal word: " + word)

            scale, increment = numwords[word]

        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current

def get_quantity(sentence):
    #Find a quantity value from a sentence
    tokens = tokenize(sentence)
    for word in tokens:
        if word in ("last", "final"):
            return -1
        try:
            q = text2int(word)
        except:
            pass
        else:
            return q
    return None