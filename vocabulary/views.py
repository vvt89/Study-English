from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import sqlite3
from .create_database import *

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import AddNewForm

# Create your views here.

@login_required
def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    username = request.user.get_username()
    #username = 'None'
    #print("USERNAME: ", username)
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    file_name = 'D:/Projects/PythonStudy/studyenglish/databases/' + username + '_english_vocabulary.sqlite'

    ## Uncomment to deploy to PythonAnywhere:
    # file_name = '/home/vvt89/Study-English/' + file_name

    try:
        res = add_new_word(file_name, 'cat')
    except:
        conn = sqlite3.connect(file_name)
        #print("FILENAME: ", file_name)
        cur = conn.cursor()
        cur.execute('CREATE TABLE Words (id INTEGER, word TEXT)')
        conn.commit()
        cur.close()
        res = add_new_word(file_name, 'cat')

    random_word = get_random_word_from_the_last(file_name, max((res[3]-1), 1))
    path = 'D:/Projects/PythonStudy/studyenglish/databases/'
    trans_file_name = path + username + '_translate_english_vocabulary.sqlite'
    translations = get_translation_by_number(trans_file_name, random_word[1])

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_words': res[3]+1, 'random_word': random_word, 'num_visits': num_visits, 'translations': translations},
    )


@login_required
def add_new_word_from_form(request):
    # Если данный запрос типа POST, тогда
    if request.method == 'POST':

        # Создаем экземпляр формы и заполняем данными из запроса (связывание, binding):
        form = AddNewForm(request.POST)

        # Проверка валидности данных формы:
        if form.is_valid():
            username = request.user.get_username()
            path = 'D:/Projects/PythonStudy/studyenglish/databases/'
            file_name = path + username + '_english_vocabulary.sqlite'
            trans_file_name = path + username + '_translate_english_vocabulary.sqlite'
            # print("FORM_DATA: ", form.clean_data()[0], form.clean_data()[1])
            # Обработка данных из form.cleaned_data
            (word, translation) = form.clean_data()
            add_translation(file_name, trans_file_name, word, translation)
            # Переход по адресу 'index':
            return HttpResponseRedirect(reverse('index'))  # Сделать HTML для подтверждения!!!!!!!!!!!

    # Если это GET (или какой-либо еще), создать форму по умолчанию.
    else:
        form = AddNewForm()

    return render(request, 'vocabulary/add_new_word.html', {'form': form})
