import re


def get_docs(documents, delimiter='%'):
    return documents.split(delimiter)


def remove_punctuations(docs):
    return list(map(lambda s: re.sub(r"[^\w\d'\s]+", '', s), docs))


def remove_next_tab_chars(docs):
    return list(map(lambda s: s.replace('\n', ' ').replace('\t', ' '), docs))


def remove_extra_whitespaces(docs):
    return list(map(lambda s: ' '.join(s.split()), docs))
