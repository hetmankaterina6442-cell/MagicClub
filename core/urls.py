# core/urls.py
from django.urls import path
from . import views, views_quiz

app_name = "core"

urlpatterns = [
    path('', views.core, name='index'),
    path('posts/<slug:slug>/', views.post_detail, name='post_detail'),
    path('posts/<slug:slug>/comment/', views.post_comment, name='post_comment'),

        # сторінка зі всіма тестами
    path('quizzes/', views.quiz_list, name='quiz_list'),
    # отримати тест за slug (для попапа)
    path('quiz/<slug:slug>/get/', views.quiz_get, name='quiz_get'),


    # КВІЗ API
    path('quiz/random/', views_quiz.quiz_random, name='quiz_random'),
    path('quiz/submit/', views_quiz.quiz_submit, name='quiz_submit'),

    # опитування
    path('poll/vote/<slug:slug>/', views.poll_vote, name='poll_vote'),
    path('poll/results/<slug:slug>/', views.poll_results, name='poll_results'),
]

