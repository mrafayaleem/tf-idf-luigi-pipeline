import math

from collections import Counter
from collections import OrderedDict
from copy import deepcopy


def get_term_frequencies(docs):
    tfreq = {}
    tfreqlog = {}

    for i, doc in enumerate(docs):
        tfd = Counter(doc.split())
        tfreq[i] = tfd

        tfdlog = deepcopy(tfd)

        # Take log10 of all the counts to normalize
        for k, v in tfdlog.items():
            tfdlog[k] = math.log10(v + 1)

        tfreqlog[i] = tfdlog

    return tfreq, tfreqlog


def get_normalized_term_frequencies(docs):
    tfreq = {}
    tfreq_norm = {}

    for i, doc in enumerate(docs):
        words = doc.split()
        doc_length = len(words)
        tfd = Counter(words)
        tfreq[i] = tfd

        tfdnorm = deepcopy(tfd)
        for k, v in tfdnorm.items():
            tfdnorm[k] /= doc_length

        tfreq_norm[i] = tfdnorm

    return tfreq, tfreq_norm


def get_vocab(docs):
    words = []
    for doc in docs:
        words.extend(doc.split())

    terms = OrderedDict.fromkeys(words).keys()
    return terms, len(terms)


def get_idfs(docs, terms, tfreq_d, N):
    idf = {}

    for term in terms:
        df_t = 0
        for i, doc in enumerate(docs):
            if tfreq_d[i][term] > 0:
                df_t += 1

        idf[term] = math.log10(N / df_t)

    return idf


def get_word_term_doc_matrix(terms, docs, tfreq_norm, idf):
    word_term_doc = []
    for term in terms:
        scores = [term]
        for i, doc in enumerate(docs):
            scores.append(tfreq_norm[i][term] * idf[term])

        word_term_doc.append(scores)

    return word_term_doc
