from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import User

#from matplotlib.style import context
#from django.http import HttpResponse, JsonResponse
#from pickletools import read_unicodestringnl

from django.contrib.auth.hashers import make_password, check_password #비밀번호 암호화 / 패스워드 체크(db에있는거와 일치성확인)
from . import movSel
from . import movie10


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
            movie_id = myuser_info.usermovieid
            context.update(movSel.getMoviedata(movie_id))
            context['movie_list'] = [movSel.getMoviedata(x) for x in movie10.print_similar_movies(movie_id)]
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
'''
def csvTomodel(request):
    #csv파일을 DB에 넣는 작업을 할 곳입니다.

    #바로 아래 주석처리된 이건 자꾸 typeerror가 나서 버렸습니다
    #movie_id를 int인거 확인했는데 자꾸 숫자가 아닌게 들어갔다고 뜹니다.
    #https://continuous-development.tistory.com/105 를 참고했습니다.
    """
    path = 'C:/Users/Coke/playground/Section5/cp1project/CP1Project/moviya/user/data/m_list.csv'
    file = open(path, 'r', encoding="UTF-8")
    reader = csv.reader(file)
    print('------', reader)

    list = []
    for row in reader:
        list.append(Movie(
            movie_id=row[0],
            title=row[1],
            genres=row[2]))
    
    Movie.objects.bulk_create(list)

    path2 = 'C:/Users/Coke/playground/Section5/cp1project/CP1Project/moviya/user/data/filtered_rate.csv'
    file2 = open(path2, 'r', encoding="UTF-8")
    reader2 = csv.reader(file2)
    print('------', reader)

    list2 = []
    for row in reader2:
        list2.append(Rate(
            movie_id=row[0],
            mean=row[1],
            count=row[2],
            username=row[3],
            rating=row[4]))
    
    Rate.objects.bulk_create(list2)    

    return HttpResponse('create model')
    """
    #이건 https://fierycoding.tistory.com/64 를 참고했습니다.
    data = None
    file_dir = 'C:/Users/Coke/playground/Section5/cp1project/CP1Project/moviya/user/data/'

    def read_data(table_name):
        with open(file_dir + f'{table_name}.csv', 'r', encoding='UTF-8') as csvfile:
            reader = csv.reader(csvfile)
            global data
            data = list(reader)
        return
    
    def footer(table_name, class_name, bulk_list):
        class_name.objects.bulk_create(bulk_list)
        
        with open(file_dir + f'{table_name}.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
        return
    
    
    #m_list테이블을 만들기 위한 m_list테이블
    read_data('m_list')
    if not data:
        return HttpResponse('Nothing to update') #데이터가 없다고 떠서 진행 못하는 중입니다.

    arr = []
    for row in data:
        arr.append(Movie(
            movie_id=row[0],
            title=row[1],
            genres=row[2]))

    footer('m_list', Movie, arr)

    #pivot테이블을 만들기 위한 레이트테이블
    read_data('filtered_rate')
    if not data:
        return HttpResponse('Nothing to update')

    arr = []
    for row in data:
        arr.append(Rate(
            movie_id=row[0],
            mean=row[1],
            count=row[2],
            username=row[3],
            rating=row[4]))
            
    footer('filtered_rate', Rate, arr)
    return HttpResponse('Rate table updated')


def mainpage(request):
    #이건 나중에 movie10(동현님 모델)이랑 연결하려고 만든 페이지입니다.
    return HttpResponse(a)
'''
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
