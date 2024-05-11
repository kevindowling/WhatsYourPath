# quizzes/urls.py

from django.urls import include, path
from . import views
from .views import QuizListView,CustomAuthToken

urlpatterns = [
    path('', views.list_quizzes, name='list_quizzes'),
    path('<int:quiz_id>/', views.take_quiz, name='take_quiz'),  # Corrected path for quiz details
    path('<int:quiz_id>/submit/<int:question_id>/<int:question_index>/', views.submit_answer, name='submit_answer'),
    path('<int:quiz_id>/show_results', views.submit_quiz, name='show_results'),
    path('api/', include([
        path('quizzes/', QuizListView.as_view(), name='api-quiz-list'),
        path('auth/', CustomAuthToken.as_view(), name='authenticate'),
    ])),
]
