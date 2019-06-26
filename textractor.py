import re
from itertools import groupby


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


one_gram_stopwords =['experience', 'data', 'science', 'learning', 'machine', 'skills', 'years', 'ability', 'computer',
                     'etc', 'analysis', 'degree', 'statistical', 'knowledge', 'strong', 'modeling', 'working',
                     'techniques','work', 'quantitative', 'engineering', 'preferred', 'field', 'excellent',  'plus',
                     'understanding', 'programming','2', '3', 'applied', 'models', 'technical', 'tools', 'languages',
                     'large','solving', 'using', 'research','related', 'advanced', 'business', 'problem', 'problems',
                     'learn', 'product', 'least', 'team', 'software', 'master', 'phd', 'e', 'complex', 'technologies',
                     'proficiency', 'ms', '1', 'analytical', 'development', 'processing', 'results', 'math', 'one',
                     'management', 'relevant', 'environment', 'end', 'e', 'g', 'concepts','predictive', 'building',
                     'sets']

one_gram_stopwords.extend(stopwords)


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


trigram_list = []
bigram_list = []
words = {}

path = "data scientit skills.txt"

with open(path, "r") as fob:
    for line in fob:
        word_list = re.split(r"[^a-zA-Z0-9\\']", line)
        word_list[:] = [word.lower() for word in word_list if word.lower() not in [""]]

        for i in range(len(word_list) - 2):

            trigram_sentence = [word_list[i], word_list[i+1], word_list[i+2]]
            trigram_list.append(" ".join(sorted(trigram_sentence)))

            bigram_sentence = [word_list[i], word_list[i + 1]]
            bigram_list.append(" ".join(sorted(bigram_sentence)))

            if i == len(word_list)-3:
                bigram_sentence = [word_list[i+1], word_list[i + 2]]
                bigram_list.append(" ".join(sorted(bigram_sentence)))

        word_list[:] = [word.lower() for word in word_list if word.lower() not in one_gram_stopwords]

        for word in word_list:
            if word in words:
                words[word] += 1
            else:
                words[word] = 1


trigrams = generate_dict(trigram_list)
bigrams = generate_dict(bigram_list)

collection = {"words": words, "two grams": bigrams, "three grams": trigrams}

for item in collection:
    print "Top 10 ", item
    result(collection[item], 10)









