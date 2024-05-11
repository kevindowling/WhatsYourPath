
from datetime import datetime
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_http_methods
from quizmaker.models import Quiz, Question, Answer, AttributeThreshold, AnswerAttribute, UserQuizAttempt, UserAnswer, OutcomeCode
from django.utils import timezone
import logging

## API ##
from rest_framework.generics import ListAPIView
from quizmaker.models import Quiz
from quizmaker.serializers import QuizSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

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
        attribute_threshold_values_dict[attribute_threshold.AttributeName] = attribute_threshold.ThresholdValue

    user_answers = UserAnswer.objects.filter(Attempt=quiz_attempt)

    for user_answer in user_answers: 
        answer_attributes = AnswerAttribute.objects.filter(Answer=user_answer.Answer)
        for answer_attribute in answer_attributes:
            attribute_threshold_values_dict[answer_attribute.AttributeName] -= answer_attribute.Weight

    for attribute_threshold in attribute_thresholds:
        if(attribute_threshold_values_dict[attribute_threshold.AttributeName] < attribute_threshold.ThresholdValue):
            attribute_threshold_values_dict[attribute_threshold.AttributeName] = attribute_threshold.RightCodeString
        else: 
            attribute_threshold_values_dict[attribute_threshold.AttributeName] = attribute_threshold.LeftCodeString

    combination_code_str= ''.join(attribute_threshold_values_dict.values())

    
 

    try:
        outcome_code = OutcomeCode.objects.get(Quiz=quiz_attempt.Quiz, CombinationCode=combination_code_str)
    except OutcomeCode.DoesNotExist:
            logger.debug("No outcome code found for the given quiz and combination code.")


    quiz_attempt.CompletedAt = timezone.now()

    return outcome_code.Description
    

## API ##
class QuizListView(ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

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