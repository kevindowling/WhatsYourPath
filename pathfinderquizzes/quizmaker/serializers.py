from rest_framework import serializers
from django.utils import timezone
from .models import Quiz, Question, Answer, AnswerAttribute, UserQuizAttempt, UserAnswer, OutcomeCode
import logging

logger = logging.getLogger('myapp.custom')

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
    attributes = AnswerAttributeSerializer(many=True)

    class Meta:
        model = Answer
        fields = ['AnswerID', 'Text', 'attributes']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['QuestionID', 'Text', 'CreatedAt', 'QuestionType', 'Sequence', 'answers']

class OutcomeCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutcomeCode
        fields = ['OutcomeCodeID', 'CombinationCode', 'Description']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    outcomecodes = OutcomeCodeSerializer(many=True) 
    logger.debug("Quiz Serializer called")
    class Meta:
        model = Quiz
        fields = ['QuizID', 'Title', 'Description', 'QuizCategory', 'CreatedBy', 'IsPublished', 'questions', 'outcomecodes']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        outcomecodes_data = validated_data.pop('outcomecodes', [])
        quiz = Quiz.objects.create(**validated_data)

        for question_data in questions_data:
            answers_data = question_data.pop('answers')
            question = Question.objects.create(Quiz=quiz, **question_data)

            for answer_data in answers_data:
                attributes_data = answer_data.pop('attributes', [])
                answer = Answer.objects.create(Question=question, **answer_data)

                for attribute_data in attributes_data:
                    AnswerAttribute.objects.create(Answer=answer, **attribute_data)

        for outcome_data in outcomecodes_data:
            OutcomeCode.objects.create(Quiz=quiz, **outcome_data)

        return quiz

