import math

from collections import Counter
from collections import OrderedDict
from copy import deepcopy


def get_term_frequencies(docs):
    """ Given a list of docs, it generated term frequencies and log10 of term frequencies and returns both of them.

    :param docs:
    :return: term frequency and log10 of term frequency as separate dict indexed on doc id and containing frequencies
    for all the words for that doc
    """
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
    """ Given a list of docs, it generated term frequencies and normalized term frequencies and returns both of them.

    :param docs:
    :return: term frequency and normalized term frequency as separate dict indexed on doc id and containing frequencies
    for all the words for that doc
    """
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
    """ Returns unique terms in the corpus along with the vocabulary size.

    :param docs:
    :return: (terms, vocab_size)
    """
    words = []
    for doc in docs:
        words.extend(doc.split())

    terms = OrderedDict.fromkeys(words).keys()
    return terms, len(terms)


def get_idfs(docs, terms, tfreq_d, N):
    """ Generates inverse document frequency for each term in the vocabulary.

    :param docs:
    :param terms:
    :param tfreq_d:
    :param N: number of documents
    :return: inverse document frequency for every term
    """
    idf = {}

    for term in terms:
        df_t = 0
        for i, doc in enumerate(docs):
            if tfreq_d[i][term] > 0:
                df_t += 1

        idf[term] = math.log10(N / df_t)

    return idf


def get_word_term_doc_matrix(terms, docs, tfreq_norm, idf):
    """ Generates tf-idf weight matrix for every term and the document.

    :param terms:
    :param docs:
    :param tfreq_norm:
    :param idf:
    :return: tf-idf weight matrix
    """
    word_term_doc = []
    for term in terms:
        scores = [term]
        for i, doc in enumerate(docs):
            scores.append(tfreq_norm[i][term] * idf[term])

        word_term_doc.append(scores)

    return word_term_doc
