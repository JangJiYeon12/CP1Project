from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register ,name = 'register'),
    path('login/', views.login ,name = 'login' ),
    path('logout/', views.logout ,name = 'logout' ),
    path('searchmovie/', views.SearchMovie ,name = 'searchmovie' ),
    path('movview/', name = 'movview' ),
    path('movSel/', name = 'movSel' ),
]