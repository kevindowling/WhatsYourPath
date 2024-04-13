
from datetime import datetime
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_http_methods
from quizmaker.models import Quiz, Question, Answer, AttributeThreshold, AnswerAttribute, UserQuizAttempt, UserAnswer, OutcomeCode
from django.utils import timezone
import logging

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
    
    attempt, created = UserQuizAttempt.objects.get_or_create(
        Quiz=quiz,
        User=user,
        defaults={'StartedAt': timezone.now()}
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
    submit_quiz = False

    quiz = get_object_or_404(Quiz, pk=quiz_id)
    user = request.user
    question = get_object_or_404(Question, pk=question_id)
    answer_id = request.POST.get('selected_answer')
    answer = get_object_or_404(Answer, pk=answer_id)

    last_question = Question.objects.filter(Quiz=quiz).order_by('Sequence').last()
    if(last_question.pk == question_id):
        submit_quiz = True

    attempt = UserQuizAttempt.objects.get(Quiz=quiz, User=user)

    # Create a UserAnswer
    user_answer = UserAnswer.objects.create(
        Attempt=attempt,
        Question=question,
        Answer=answer,
        AnsweredAt= timezone.now()
    )    

    if(submit_quiz): 
        #Grade quiz. Need outcome codes created before this point. 
        content = {
            'attempt_id': attempt.pk
        }
        return render(request, 'quizzes/show_results.html', content)

    # Redirect to a new page or the next question
    return render(request, 'quizzes/take_quiz.html', {
        'quiz': quiz,
        'attempt': attempt,
        'question_index': question_index,
    })


def submit_quiz(request, attempt_id):
    quiz = get_object_or_404(UserQuizAttempt, pk=attempt_id)
    user_answers = UserAnswer.objects.filter(Quiz=quiz)
    for user_answer in user_answers: 
        answer = get_object_or_404(Answer, pk=user_answer.Answer)
        logger.debug(answer)
    pass
