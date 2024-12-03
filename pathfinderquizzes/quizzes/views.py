
from datetime import datetime
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_http_methods
from quizmaker.models import Quiz, Question, Answer, AttributeThreshold, AnswerAttribute, UserQuizAttempt, UserAnswer, OutcomeCode
from django.utils import timezone
import logging

## API ##
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from quizmaker.serializers import QuizSerializer, QuestionSerializer, UserQuizAttemptSerializer, QuizSummarySerializer

logger = logging.getLogger('myapp.custom')

# Create your views here.
def list_quizzes(request):
    quizzes = Quiz.objects.filter(IsPublished=True)  # Example filter for published quizzes
    return render(request, 'quizzes/list_quizzes.html', {'quizzes': quizzes})

def take_quiz(request, quiz_id, question_index=0):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    user = request.user

    # Fetch the first question by order or sequence
    current_question = Question.objects.filter(Quiz=quiz).order_by('Sequence')[question_index]
    # Fetch answers for the first question
    answers = Answer.objects.filter(Question=current_question)
    # Comment
    attempt = UserQuizAttempt.objects.create(
        Quiz=quiz,
        User=user,
        StartedAt = timezone.now()
    )




    return render(request, 'quizzes/take_quiz.html', {
        'quiz': quiz,
        'question': current_question,
        'answers': answers,
        'attempt': attempt,
        'question_index': question_index,
    })

@require_http_methods(["POST"])
def submit_answer(request, quiz_id, question_id, question_index):
    submit = False

    quiz = get_object_or_404(Quiz, pk=quiz_id)
    user = request.user
    question = get_object_or_404(Question, pk=question_id)
    answer_id = request.POST.get('selected_answer')
    answer = get_object_or_404(Answer, pk=answer_id)


    last_question = Question.objects.filter(Quiz=quiz).order_by('Sequence').last()
    if(last_question.pk == question_id):
        submit = True

    attempt = UserQuizAttempt.objects.filter(Quiz=quiz, User=user).order_by('-StartedAt').first()

    # Create a UserAnswer
    user_answer = UserAnswer.objects.create(
        Attempt=attempt,
        Question=question,
        Answer=answer,
        AnsweredAt= timezone.now()
    )    




    if(submit): 
        results = submit_quiz(request, attempt.AttemptID)
        return render(request, 'quizzes/show_results.html', {
            'results': results
    })

    question_index+=1
    current_question = Question.objects.filter(Quiz=quiz).order_by('Sequence')[question_index]
    answers = Answer.objects.filter(Question=current_question)


    # Redirect to a new page or the next question
    return render(request, 'quizzes/take_quiz.html', {
        'quiz': quiz,
        'question': current_question,
        'answers': answers,
        'attempt': attempt,
        'question_index': question_index,
    })


def submit_quiz(request, attempt_id):
    quiz_attempt = get_object_or_404(UserQuizAttempt, pk=attempt_id)
    attribute_thresholds = AttributeThreshold.objects.filter(Quiz=quiz_attempt.Quiz)
    attribute_threshold_values_dict = {}
    for attribute_threshold in attribute_thresholds:
        attribute_threshold_values_dict[attribute_threshold.AttributeName] = 0

    user_answers = UserAnswer.objects.filter(Attempt=quiz_attempt)

    for user_answer in user_answers: 
        answer_attributes = AnswerAttribute.objects.filter(Answer=user_answer.Answer)
        for answer_attribute in answer_attributes:
            attribute_threshold_values_dict[answer_attribute.AttributeName] += answer_attribute.Weight
    for attribute_threshold in attribute_thresholds:
        if(attribute_threshold_values_dict[attribute_threshold.AttributeName] >= attribute_threshold.ThresholdValue):
            attribute_threshold_values_dict[attribute_threshold.AttributeName] = attribute_threshold.RightCodeString
        else: 
            attribute_threshold_values_dict[attribute_threshold.AttributeName] = attribute_threshold.LeftCodeString

    combination_code_str= ''.join(attribute_threshold_values_dict.values())

    
 
    outcome_description = 'You took a quiz... And we\'re not sure what the result was. The quiz\'s creator didn\'t tell us what to do if you got this far..'
    try:
        outcome_code = OutcomeCode.objects.get(Quiz=quiz_attempt.Quiz, CombinationCode=combination_code_str)
        outcome_description = outcome_code.Description
    except OutcomeCode.DoesNotExist:
            logger.debug("No outcome code found for the given quiz and combination code.")
            


    quiz_attempt.CompletedAt = timezone.now()

    return outcome_description
    

## API ##
class QuizListView(ListAPIView):
    
    queryset = Quiz.objects.filter(IsPublished=True)  
    serializer_class = QuizSummarySerializer
    permission_classes = [IsAuthenticated]
    

class QuizDetailView(RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        quiz = self.get_object()
        quiz_data = QuizSerializer(quiz).data
        questions = Question.objects.filter(Quiz=quiz)
        questions_data = QuestionSerializer(questions, many=True).data
        quiz_data['questions'] = questions_data
        return Response(quiz_data)

class UserQuizAttemptCreateView(CreateAPIView):
    queryset = UserQuizAttempt.objects.all()
    serializer_class = UserQuizAttemptSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(User=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data
        data['StartedAt'] = timezone.now()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        quiz_attempt = serializer.save(User=request.user)

        # Grading the attempt
        attribute_threshold_values_dict = {}
        user_answers = UserAnswer.objects.filter(Attempt=quiz_attempt)
        
        for user_answer in user_answers:
            for attr in user_answer.Answer.answerattribute_set.all():
                if attr.AttributeName not in attribute_threshold_values_dict:
                    attribute_threshold_values_dict[attr.AttributeName] = attr.Weight
                else:
                    attribute_threshold_values_dict[attr.AttributeName] += attr.Weight
        # Compare with thresholds
        attribute_thresholds = AttributeThreshold.objects.filter(Quiz=quiz_attempt.Quiz)
        for attribute_threshold in attribute_thresholds:
            if attribute_threshold.AttributeName in attribute_threshold_values_dict:
                if attribute_threshold_values_dict[attribute_threshold.AttributeName] > attribute_threshold.ThresholdValue:
                    attribute_threshold_values_dict[attribute_threshold.AttributeName] = attribute_threshold.RightCodeString
                else:
                    attribute_threshold_values_dict[attribute_threshold.AttributeName] = attribute_threshold.LeftCodeString

        combination_code_str = ''.join(attribute_threshold_values_dict.values())

        try:
            outcome_code = OutcomeCode.objects.get(Quiz=quiz_attempt.Quiz, CombinationCode=combination_code_str)
        except OutcomeCode.DoesNotExist:
            outcome_code = None

        quiz_attempt.CompletedAt = timezone.now()
        quiz_attempt.save()

        response_data = {
            'quiz_attempt': UserQuizAttemptSerializer(quiz_attempt).data,
            'outcome': outcome_code.Description if outcome_code else "No outcome code found"
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
        
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })