import requests


api_key = 'bd7066a3afac2a57330952c5ad6591cd'
BASE_URL = 'https://api.themoviedb.org/3'

def imgconfig(wsize) :
    url = BASE_URL+'/configuration'
    params = {
        'api_key' : api_key
    }
    resp = requests.get(url,params)
    data = resp.json()['images']
    return data['base_url'],data[wsize]

IMG_BASE_URL, IMG_SIZE = imgconfig('poster_sizes')

def Searmov(query) : 
    url = BASE_URL + '/search/movie'
    params = {
        'api_key' : api_key,
        'query' : query,
        'language' : 'ko'
    }

    resp = requests.get(url, params=params)
    data = resp.json()['results']
    return data

def getMoviedata(movie_id) :
    url = BASE_URL + f'/movie/{movie_id}'
    params = {
        'api_key' : api_key,
        'language' : 'ko'
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    return data
