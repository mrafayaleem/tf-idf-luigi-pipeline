import pandas as pd

from scipy.spatial.distance import pdist, squareform
from sklearn.metrics.pairwise import euclidean_distances


def convert_to_df(word_term_doc, N):
    """ Converts tf-idf weight matrix to a pandas df.

    :param word_term_doc:
    :param N:
    :return: df
    """
    columns = ['term'] + [i for i in range(N)]
    return pd.DataFrame(word_term_doc, columns=columns).set_index(['term'])


def get_euclid_df_sklearn(df, N):
    """ Calculates euclidean distance between all the document vectors using scikit-learn

    :param df:
    :param N:
    :return: N x N df containing euclidean distances
    """
    no_index = df.reset_index(drop=True)
    values = [no_index.values[i] for i in range(N)]
    dist = euclidean_distances(values)
    return pd.DataFrame(dist)


def get_euclid_df_scipy(df, N):
    """ Calculates euclidean distance between all the document vectors using scipy

    :param df:
    :param N:
    :return: N x N df containing euclidean distances
    """
    no_index = df.reset_index(drop=True)
    values = [no_index.values[i] for i in range(N)]
    dist = pdist(values, 'euclidean')
    return pd.DataFrame(squareform(dist))


def get_similarity_df(euclid_df, N):
    """ Generates a similarity data frame for each doc against all the other docs satisfying the following:

        document_id_1 < document_id_2

    :param euclid_df:
    :param N:
    :return: df
    """
    similarities = []
    for i in range(N):
        for j in range(i + 1, N):
            dist = euclid_df[i][j]
            similarities.append((i, j, dist))

    return pd.DataFrame(similarities)
