import re
import pandas as pd
from itertools import groupby
import time

start_time = time.time()


stopwords = ["",'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll",
             "you'd",'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her',
             'hers','herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what',
             'which','who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were','be',
             'been','being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the','and','but',
             'if','or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
             'between','into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
             'in','out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when',
             'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
             'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don',
             "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't",
             'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven',
             "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan',
             "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn',
             "wouldn't", 'experience']


one_gram_stopwords =['experience', 'data', 'learning', 'etc', 'high', 'testing', 'science', 'computer', 'statistics',
                     'analytics', 'mathematics', 'methods', 'machine', 'skills', 'years', 'ability', 'operations',
                     'projects', 'high', 'etc', 'analysis', 'degree', 'statistical', 'knowledge', 'strong', 'working',
                     'techniques', 'work', 'quantitative', 'engineering', 'preferred', 'field', 'excellent',  'plus',
                     'understanding', 'programming', '2', '3', 'applied', 'models', 'technical', 'tools', 'languages',
                     'large','solving', 'using', 'research','related', 'advanced', 'business', 'problem', 'problems',
                     'learn', 'product', 'least', 'team', 'software', 'master', 'bachelor','phd', 'e', 'complex', 'technologies',
                     'proficiency', 'ms', '1', 'analytical', 'development', 'processing', 'results', 'math', 'one',
                     'management', 'relevant', 'environment', 'end', 'e', 'g', 'concepts','predictive', 'building',
                     'sets', 'written', 'including', 'familiarity', 'year', 'required', 'discipline', 'good',
                     'method', 'multiple', 'able', 'level', 'hands', 'role', 'following', 'equivalent', 'minimum',
                     'physics', 'ph', 'language', 'similar', 'verbal', 'Proficient', 'Scripting']

data_skills = ['modeling', 'communication', 'visualization', 'algorithms', 'mining', 'big', 'scripting'] 
one_gram_stopwords.extend(stopwords)
one_gram_stopwords.extend(data_skills)


def gen_word_list(line,  stopwords):
    word_list = re.split(r"[^a-zA-Z0-9\\']", line)
    word_list[:] = [word.lower() for word in word_list if word.lower() not in stopwords]
    return word_list


def update_dict(ngram_dict,ngram_sentence):
    if ngram_sentence in ngram_dict:
        ngram_dict[ngram_sentence] += 1
    else:
        ngram_dict[ngram_sentence] = 1


def generate_dict(sentence_list):
    sorted_sentences = sorted(sentence_list)
    vocab = {}
    for _, similar_sentences in groupby(sorted_sentences):
        similar_sentences = list(similar_sentences)
        vocab[similar_sentences[0]] = len(similar_sentences)
    return vocab


def result(vocab, size):
    lst = sorted(vocab.items(), key=lambda x: x[1], reverse=True)[:size]
    for string, freq in lst:
        print (string, freq)
    return lst


def unordered_ngram(fob,one_gram_stopwords, stopwords): #Order of word in a senetence does not matter

    trigram_list = []
    bigram_list = []
    words = {}

    for line in fob:
        word_list = gen_word_list(line, stopwords)

        for i in range(len(word_list) - 2):
            string = [word_list[i], word_list[i + 1], word_list[i + 2]]
            trigram_list.append(" ".join(sorted(string)))

        for i in range(len(word_list) - 1):
            string = [word_list[i], word_list[i + 1]]
            bigram_list.append(" ".join(sorted(string)))

        word_list = gen_word_list(line, one_gram_stopwords)

        for word in word_list:
            update_dict(words, word)

    return trigram_list, bigram_list, words


def ordered_ngram(fob,  one_gram_stopwords,stopwords):
    trigram_dict = {}
    bigram_dict = {}
    words = {}

    for line in fob:
        word_list = gen_word_list(line, stopwords)

        for i in range(len(word_list) - 2):
            trigram_sentence = " ".join([word_list[i], word_list[i + 1], word_list[i + 2]])
            update_dict(trigram_dict, trigram_sentence)

        for i in range(len(word_list) - 1):
            bigram_sentence = " ".join([word_list[i], word_list[i + 1]])
            update_dict(bigram_dict, bigram_sentence)

        word_list = gen_word_list(line, one_gram_stopwords)

        for word in word_list:
            update_dict(words, word)

    return trigram_dict, bigram_dict, words



path = "data scientit skills.txt"

# Two options: Choose an option by uncommenting it, make sure to comment out the other option.


# Option 1: The order of individual elements in a ngram sentence doesn't matter:
# Eg: "Computer science  statistics" and "statistics and computer science" will be treated as the same

with open(path, "r") as fob:
    trigram_list, bigram_list, words = unordered_ngram(fob, one_gram_stopwords, stopwords)
    trigrams = generate_dict(trigram_list)
    bigrams = generate_dict(bigram_list)
    


# Option 1 ends


# Option 2 : If you want to preserved the order of words in ngram
# Eg: "r python sql" and "python sql r" will be treated differently.


# with open(path, "r") as fob:
#     trigrams, bigrams, words = ordered_ngram(fob, stopwords)

# Option 2 ends



collection = {"words": words, "two grams": bigrams, "three grams": trigrams}

for item in collection:
    print "Top 10 ", item
    result(collection[item], 20)


res = result(words, 25)  # Sorts and returns the word count


pd.DataFrame(res).to_excel('Top25Skills.xlsx', header=["Word", "counts"], index=False)






