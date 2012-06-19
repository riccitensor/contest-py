__author__ = 'cw'
import recsys.algorithm
from recsys.algorithm.factorize import SVD
from recsys.utils.svdlibc import SVDLIBC

LOAD = False

if LOAD:
    svd = SVD(filename='/tmp/movielens_1M') # Loading already computed SVD model
else:
    svd = SVD()
    svd.load_data(filename='./data/plista/impression_10000', sep='::',
        format={'col': 0, 'row': 1, 'value': 2, 'ids': int})

    recsys.algorithm.VERBOSE = True

    k = 100
    svd.compute(k=k, min_values=10, pre_normalize=None, mean_center=True, post_normalize=True,
        savefile='/tmp/movielens_1M')

ITEMID1 = 1    # Toy Story (1995)
ITEMID2 = 2355 # A bug's life (1998)
svd.similarity(ITEMID1, ITEMID2)

MIN_RATING = 0.0
MAX_RATING = 5.0
ITEMID = 1
USERID = 1
svd.predict(ITEMID, USERID, MIN_RATING, MAX_RATING)

svd.get_matrix().value(ITEMID, USERID)
"""
svd.recommend(USERID, is_row=False) #cols are users and rows are items, thus we set is_row=False

svd.recommend(ITEMID)
"""