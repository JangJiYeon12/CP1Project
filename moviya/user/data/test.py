import pickle
from sklearn.neighbors import NearestNeighbors
import pandas as pd



def print_similar_movies(index) :

    m_list = pd.read_csv('m_data.csv', error_bad_lines=False, engine ='python')


    loaded_model = pickle.load(open('knnpickle_file', 'rb'))
    loaded_data = pickle.load(open('eda_data', 'rb'))

    #피클 불러오기

    loaded_model.fit(loaded_data)
    
    index_movie_rate = loaded_data.loc[index,:].values.reshape(1,-1)

    #가장 가까운 10편의 영화와 지정된 영화와의 거리를 구합니다.
    distances,indices = loaded_model.kneighbors(index_movie_rate,n_neighbors = 11) 

    movie_list=[]

    for i in range(0,len(distances.flatten())):
        
        get_movie = m_list.loc[m_list['id']==index]['title']
        
        if i==0:
            pass
        else :
            indices_flat = indices.flatten()[i]
            
            get_movie = m_list.loc[m_list['id']==loaded_data.iloc[indices_flat,:].name]['title']

            movie_list.append(get_movie.to_frame().reset_index().set_index('index'))

    m = pd.DataFrame()   
    for i in movie_list:
        m = pd.concat([m,i])
    m = m.reset_index()
    m.columns = ['영화코드','영화명']
    return m

print(print_similar_movies(791373))