from rest_framework import serializers
from django.utils import timezone
from .models import Quiz, Question, Answer, AnswerAttribute, UserQuizAttempt, UserAnswer, OutcomeCode

class UserAnswerSerializer(serializers.ModelSerializer):
    AnsweredAt = serializers.DateTimeField(required=False)

    class Meta:
        model = UserAnswer
        fields = ['Question', 'Answer', 'AnsweredAt']

    def create(self, validated_data):
        if 'AnsweredAt' not in validated_data:
            validated_data['AnsweredAt'] = timezone.now()
        return super().create(validated_data)

class UserQuizAttemptSerializer(serializers.ModelSerializer):
    answers = UserAnswerSerializer(many=True, write_only=True)
    answers_list = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserQuizAttempt
        fields = ['Quiz', 'StartedAt', 'CompletedAt', 'answers', 'answers_list']

    def get_answers_list(self, obj):
        answers = UserAnswer.objects.filter(Attempt=obj)
        return UserAnswerSerializer(answers, many=True).data

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        quiz_attempt = UserQuizAttempt.objects.create(**validated_data)
        for answer_data in answers_data:
            if 'AnsweredAt' not in answer_data:
                answer_data['AnsweredAt'] = timezone.now()
            UserAnswer.objects.create(Attempt=quiz_attempt, **answer_data)
        return quiz_attempt

class AnswerAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerAttribute
        fields = ['AttributeID', 'AttributeName', 'Weight']

class AnswerSerializer(serializers.ModelSerializer):
    attributes = AnswerAttributeSerializer(many=True, read_only=True, source='answerattribute_set')

    class Meta:
        model = Answer
        fields = ['AnswerID', 'Text', 'attributes']

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True, source='answer_set')

    class Meta:
        model = Question
        fields = ['QuestionID', 'Text', 'CreatedAt', 'QuestionType', 'Sequence', 'answers']

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['QuizID', 'Title', 'Description', 'QuizCategory', 'CreatedBy', 'CreatedAt', 'IsPublished']
