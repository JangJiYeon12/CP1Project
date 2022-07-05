from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from matplotlib.style import context
from .models import User

from .models import User
from django.contrib.auth.hashers import make_password, check_password #비밀번호 암호화 / 패스워드 체크(db에있는거와 일치성확인)
from . import movSel
import json

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
        myuser_info = User.objects.get(pk=user_id)
        context['username'] = myuser_info.username
        context['login'] = True
        context['setting'] = myuser_info.datasetting==True
        if myuser_info.datasetting == True :
            data = movSel.getMoviedata(myuser_info.usermovieid)
            context['movie_id'] = data['id']
            context['title'] = data['title']
            context['original_title'] = data['original_title']
            context['original_language'] = data['original_language']
            context['poster_path'] = data['poster_path']
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
            return render(request,'movSel.html',context)


        return render(request, 'searchmovie.html',response_data)

def movieSelect(request):
    context = {}
    return render(request, 'movSel.html', context) 

def movieview(request):
    title = request.GET.get('title',None)
    ori_title = request.GET.get('original_title',None)
    ori_lang = request.GET.get('original_language',None)
    poster_path = request.GET.get('poster_path',None)
    context = {
        'poster_url' : movSel.IMG_BASE_URL+movSel.IMG_SIZE[1]+poster_path,
        'moviename' : title+f"({ori_title},{ori_lang})"
    }
    return render(request, 'movview.html', context) 

def movieSelectMsg(request):
    movie_id = request.GET.get('movie_id',None)
    title = request.GET.get('title',None)
    ori_title = request.GET.get('original_title',None)
    ori_lang = request.GET.get('original_language',None)
    poster_path = request.GET.get('poster_path',None)
    context = {
        'movie_id' : movie_id,
        'title' : title,
        'original_title' : ori_title,
        'original_language' : ori_lang,
        'poster_path' : poster_path
    }
    user_id = request.session.get('user')
    user = User.objects.get(pk=user_id)
    user.datasetting = True
    user.usermovieid = movie_id
    user.save()
    return render(request, 'movSelmsg.html',context)