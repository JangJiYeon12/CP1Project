import pickle
from sklearn.neighbors import NearestNeighbors
import pandas as pd

from .models import Movie, Rate
import csv
#후에 어떤식으로 돌아갈지만 작성해 놓았습니다.

def print_similar_movies(index) :

    #아래 두줄은 DB에 저장하는 것이 성공하면 DB에서 빼내는 방식으로 바꿔줘야합니다.
    m_list = csv.reader('/data/m_list.csv')
    filtered_rate = csv.reader('/data/filtered_rate.csv')

    movie_wide = filtered_rate.pivot_table(index = 'movie_id', columns = 'username', values = 'rating').fillna(0)

    model_knn = NearestNeighbors(metric='cosine',algorithm='brute')
    model_knn.fit(movie_wide)

    index_movie_rate = movie_wide.loc[index,:].values.reshape(1,-1)

    #가장 가까운 10편의 영화와 지정된 영화와의 거리를 구합니다.
    distances,indices = model_knn.kneighbors(index_movie_rate,n_neighbors = 11) 

    
    movie_list=[]

    for i in range(0,len(distances.flatten())):
        
        get_movie = m_list.loc[m_list['movie_id']==index]['title']
        
        if i==0:
            pass
        else :
            indices_flat = indices.flatten()[i]
            
            get_movie = m_list.loc[m_list['movie_id']==movie_wide.iloc[indices_flat,:].name]['title']

            movie_list.append(get_movie.to_frame().reset_index().set_index('index'))

    m = pd.DataFrame()   
    for i in movie_list:
        m = pd.concat([m,i])
    m = m.reset_index()
    m.columns = ['영화코드','영화명']

    if m is not None:
        return '성공'
    else:
        return '실패'
