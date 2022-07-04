from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from .models import User

from .models import User
from django.contrib.auth.hashers import make_password, check_password #비밀번호 암호화 / 패스워드 체크(db에있는거와 일치성확인)
from . import movSel

import pickle
from sklearn.neighbors import NearestNeighbors
import pandas as pd
from glob import glob

# Create your views here.
def register(request):   #회원가입 페이지를 보여주기 위한 함수
    if request.method == "GET":
        return render(request, 'register.html')

    elif request.method == "POST":
        username = request.POST.get('username',None)   #딕셔너리형태
        password = request.POST.get('password',None)
        re_password = request.POST.get('re_password',None)
        res_data = {} 
        if not (username and password and re_password) :
            res_data['error'] = "모든 값을 입력해야 합니다."
            return render(request, 'register.html', res_data) #register를 요청받으면 register.html 로 응답.
        if password != re_password :
            # return HttpResponse('비밀번호가 다릅니다.')
            res_data['error'] = '비밀번호가 다릅니다.'
            return render(request, 'register.html', res_data)
        else :
            user = User(username=username, password=make_password(password))
            user.save()
            return redirect('login')

def login(request):
    response_data = {}

    if request.method == "GET" :
        return render(request, 'login.html')

    elif request.method == "POST":
        login_username = request.POST.get('username', None)
        login_password = request.POST.get('password', None)


        if not (login_username and login_password):
            response_data['error']="아이디와 비밀번호를 모두 입력해주세요."
        else : 
            myuser = User.objects.get(username=login_username) 
            #db에서 꺼내는 명령. Post로 받아온 username으로 , db의 username을 꺼내온다.
            if check_password(login_password, myuser.password):
                request.session['user'] = myuser.id 
                #세션도 딕셔너리 변수 사용과 똑같이 사용하면 된다.
                #세션 user라는 key에 방금 로그인한 id를 저장한것.
                return redirect('/user')
            else:
                response_data['error'] = "비밀번호를 틀렸습니다."

        return render(request, 'login.html',response_data)

def home(request):
    user_id = request.session.get('user')
    context = {
        'login' : False,
        'username' : None
    }
    if user_id :
        myuser_info = User.objects.get(pk=user_id)  #pk : primary key
        context['username'] = myuser_info
        context['login'] = True
        return render(request, 'home.html',context)

    return render(request, 'home.html', context) #session에 user가 없다면, (로그인을 안했다면)
    
    
def logout(request):
    request.session.pop('user')
    return redirect('/user')


def SearchMovie(request):
    response_data = {}

    if request.method == "GET" :
        return render(request, 'searchmovie.html')

    elif request.method == "POST":
        movquery = request.POST.get('searchmovie', None)


        if not movquery:
            response_data['error']="영화 제목을 입력하세요"
        else : 
            data = movSel.Searmov(movquery)
            context = {
                'movies' : data
            }
            render(request,'movSel.html',context)


        return render(request, 'searchmovie.html',response_data)

def movieSelect(request):
    context = {}
    return render(request, 'movSel.html', context) 

def movieview(request):
    moviedata = request.GET.get('moviedata',None)
    context = {
        'poster_url' : movSel.IMG_BASE_URL+movSel.IMG_SIZE[1]+moviedata['poster_path'],
        'moviename' : moviedata['title']+f"({moviedata['original_title']},{moviedata['original_language']})"
    }
    return render(request, 'movieview.html', context) 

def mainpage(request):
    #데이터와 모델을 받아옵니다
    #m_list = pd.read_csv('data/m_data.csv', error_bad_lines=False, engine ='python')
    m_list = glob("data/m_data.csv")

    loaded_model = pickle.load(open('data/knnpickle_file', 'rb'))
    loaded_data = pickle.load(open('data/eda_data', 'rb'))

    loaded_model.fit(loaded_data)

    response_data = {}

    if request.method == "GET":
        return render(request, 'register.html')

    elif request.method == "POST":
        code = request.POST.get('moviecode',None)
        code = int(code)

        if not (code):
            response_data['error']="영화 코드를 입력해주세요"
        else : 
            index_movie_rate = loaded_data.loc[code,:].values.reshape(1,-1)

            #가장 가까운 10편의 영화와 지정된 영화와의 거리를 구합니다.
            distances,indices = loaded_model.kneighbors(index_movie_rate,n_neighbors = 11)

            movie_list=[]
            m = pd.DataFrame() 

            for i in range(0,len(distances.flatten())):
                get_movie = m_list.loc[m_list['id']==code]['title']
            
                if i==0:
                    pass
                else :
                    indices_flat = indices.flatten()[i]
                    get_movie = m_list.loc[m_list['id']==loaded_data.iloc[indices_flat,:].name]['title']
                    movie_list.append(get_movie.to_frame().reset_index().set_index('index'))

            for i in movie_list:
                m = pd.concat([m,i])

            m = m.reset_index()
            m.columns = ['영화코드','영화명']
            
            response_data = m

        return render(request, 'user/mainpage.html', response_data)