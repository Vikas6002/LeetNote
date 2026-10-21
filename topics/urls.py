# topics/urls.py
from django.urls import path
from . import views

app_name = 'topics'

urlpatterns = [
    path('',        views.topic_list,   name='list'),
    path('<int:pk>/',views.topic_detail, name='detail'),
]