from django.urls import path
from .views import create_quiz, submit_attribute_thresholds, submit_questions, submit_outcome_codes

urlpatterns = [
    path('', create_quiz, name='create_quiz'),
    path('submit_attribute_thresholds/', submit_attribute_thresholds, name='submit_attribute_thresholds'),
    path('add_outcome_codes/', submit_outcome_codes, name='submit_outcome_codes'),
    path('submit_questions/', submit_questions, name='submit_questions'),

]
