import pandas as pd

from scipy.spatial.distance import pdist, squareform
from sklearn.metrics.pairwise import euclidean_distances


def get_euclid_df_sklearn(df, N):
    no_index = df.reset_index(drop=True)
    values = [no_index.values[i] for i in range(N)]
    dist = euclidean_distances(values)
    return pd.DataFrame(dist)


def get_euclid_df_scipy(df):
    no_index = df.reset_index(drop=True)
    values = [no_index.values[i] for i in range(N)]
    dist = pdist(values, 'euclidean')
    return pd.DataFrame(squareform(dist))
