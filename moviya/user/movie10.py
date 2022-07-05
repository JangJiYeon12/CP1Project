# -*- coding: utf-8 -*-
from user.apps import KNNConfig

#import pickle
#from sklearn.neighbors import NearestNeighbors


def print_similar_movies(index) :

    movie_wide = KNNConfig.data
    model_knn = KNNConfig.model
    m_list = KNNConfig.movlist

    index_movie_rate = movie_wide.loc[index,:].values.reshape(1,-1)

    distances,indices = model_knn.kneighbors(index_movie_rate,n_neighbors = 11) 


    movie_list=[]

    for i in range(1,len(distances.flatten())):
        get_movie = m_list.loc[m_list['movie_id']==index]['title']
        indices_flat = indices.flatten()[i]
        get_movie = m_list.loc[m_list['movie_id']==movie_wide.iloc[indices_flat,:].name][['movie_id','title']]
        if not get_movie.empty :
            mov = get_movie.iloc[0].tolist()[0]
            movie_list.append(mov)
    return movie_list
