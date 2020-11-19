import re


def get_docs(documents, delimiter='%'):
    """ Get document as a string and splits them by the provided delimiter.

    :param documents:
    :param delimiter:
    :return: list of documents
    """
    return documents.split(delimiter)


def remove_punctuations(docs):
    """ Removes punctuation from a list of docs.

    :param docs:
    :return: list of docs with punctuations removed
    """
    return list(map(lambda s: re.sub(r"[^\w\d'\s]+", '', s), docs))


def remove_next_tab_chars(docs):
    """ Removes nextline and tab characters from list of docs.

    :param docs:
    :return: list of docs with nextline and tab characters replaced by whitespace
    """
    return list(map(lambda s: s.replace('\n', ' ').replace('\t', ' '), docs))


def remove_extra_whitespaces(docs):
    """ Removes any extra whitespace from docs

    :param docs:
    :return: list of docs without any extra whitespaces
    """
    return list(map(lambda s: ' '.join(s.split()), docs))
