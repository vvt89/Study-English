from django.shortcuts import render

import sqlite3
from .create_database import *

# Create your views here.

def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    file_name = 'D:/Projects/PythonStudy/studyenglish/vocabulary/english_vocabulary.sqlite'
    random_word = get_random_word_from_the_last(file_name, 1)

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_words': 1234, 'random_word': random_word},
    )