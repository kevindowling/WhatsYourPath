# quizzes/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_quizzes, name='list_quizzes'),
    path('<int:quiz_id>/', views.take_quiz, name='take_quiz'),  # Corrected path for quiz details
    path('<int:quiz_id>/submit/<int:question_id>/', views.submit_answer, name='submit_answer'),
    path('<int:quiz_id>/show_results', views.submit_quiz, name='show_results')
]
