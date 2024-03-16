from django.urls import path
from .views import create_quiz, submit_attribute_thresholds, submit_questions

urlpatterns = [
    path('', create_quiz, name='create_quiz'),
    path('submit_attribute_thresholds/', submit_attribute_thresholds, name='submit_attribute_thresholds'),
    path('submit_questions/', submit_questions, name='submit_questions'),

]
