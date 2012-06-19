from recsys.utils.svdlibc import SVDLIBC

MIN_RATING = 0.0
MAX_RATING = 5.0
ITEMID1 = 1
USERID = 1

svdlibc = SVDLIBC('./data/movielens_1M/ratings.dat')
svdlibc.to_sparse_matrix(sep='::', format={'col': 0, 'row': 1, 'value': 2, 'ids': int})
svdlibc.compute(k=100)
svd = svdlibc.export()
svd.similar(ITEMID1) # results might be different than example 4. as there's no min_values=10 set here