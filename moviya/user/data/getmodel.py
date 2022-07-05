# -*- coding: utf-8 -*-
import pickle
from sklearn.neighbors import NearestNeighbors
import pandas as pd
#후에 어떤식으로 돌아갈지만 작성해 놓았습니다.

def getpickle() :

    m_list = pd.read_csv('./user/data/m_list.csv',names=['movie_id','title','genres'],encoding='utf-8')
    rev_list = pd.read_csv('./user/data/reviews.csv',encoding='utf-8')
    rev_fill = rev_list.groupby(['movie_id'],as_index=True).mean().to_dict('index')
    rev_fllist = rev_list.fillna(value=rev_fill)
    filtered_rate = pd.DataFrame(rev_fllist)
    movie_wide = pd.DataFrame(pd.pivot_table(filtered_rate,index = 'movie_id', columns = 'username', values = 'rating').fillna(0))

    model_knn = NearestNeighbors(metric='cosine',algorithm='brute')
    model_knn.fit(movie_wide)

    # Save pickle
    with open("./static/knnmodel.pickle","wb") as fw:
        pickle.dump(model_knn,fw)
    with open("./static/knndata.pickle","wb") as fw:
        pickle.dump( pd.DataFrame(movie_wide),fw)
    with open("./static/movie_list.pickle","wb") as fw:
        pickle.dump(m_list,fw)
getpickle()