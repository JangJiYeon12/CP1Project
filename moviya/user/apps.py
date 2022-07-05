# -*- coding: utf-8 -*-
from django.apps import AppConfig
import pickle

from moviya.settings import STATICFILES_DIRS

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

class KNNConfig(AppConfig):
    dirs = ''.join(STATICFILES_DIRS)
    with open(dirs+"\knnmodel.pickle","rb") as fr:
        model = pickle.load(fr)
    with open(dirs+"\knndata.pickle","rb") as fr:
        data = pickle.load(fr)
    with open(dirs+"\movie_list.pickle","rb") as fr:
        movlist = pickle.load(fr)