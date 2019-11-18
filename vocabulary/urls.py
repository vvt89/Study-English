from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path('', views.index, name='index'),  # Домашняя страница
    url(r'^add/$', views.add_new_word_from_form, name='add_new_word'),
]
