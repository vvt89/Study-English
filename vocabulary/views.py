from django.shortcuts import render

import sqlite3
from .create_database import *

# Create your views here.

def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    #file_name = 'D:/Projects/PythonStudy/studyenglish/vocabulary/english_vocabulary.sqlite'
    file_name = 'english_vocabulary.sqlite'
    ## Uncomment to deploy to PythonAnywhere:
    # file_name = '/home/vvt89/Study-English/' + file_name
    res = add_new_word(file_name, 'cat')
    #print(res)
    random_word = get_random_word_from_the_last(file_name, 1)

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_words': res[3]+1, 'random_word': random_word},
    )
