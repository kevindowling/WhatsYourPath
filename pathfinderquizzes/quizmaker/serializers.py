from rest_framework import serializers
from .models import Quiz

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['QuizID', 'Title', 'Description', 'QuizCategory', 'CreatedBy', 'CreatedAt', 'IsPublished']
