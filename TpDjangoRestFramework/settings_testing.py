from .settings import *

SECRET_KEY = 'CHANGEME!!!'
DEBUG = False

DATABASES = {
    'default':{
        'ENGINE':'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }   
}